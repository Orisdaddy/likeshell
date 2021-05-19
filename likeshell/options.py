import copy

from queue import Queue, Empty

from types import FunctionType
from typing import Union, List

from .types import Input, Options
from .context import opt_set
from .exceptions import ParameterError, DefinitionError, PARAMETER_TYPE, MISS_PARAMETER


SKIP_GETVALUE = ('Input', )


def is_input(o):
    if isinstance(o, Input):
        return True

    if hasattr(o, '__name__') and o.__name__ == 'Input':
        return True
    return False


def is_options(o):
    if isinstance(o, Options):
        return True
    return False


def assert_int(a):
    if not a.isdigit():
        error = f'"{a}" is not a int'
        raise ParameterError(PARAMETER_TYPE, arg=a, msg=error)
    return int(a)


def assert_float(a):
    try:
        arg = float(a)
    except ValueError:
        error = f'"{a}" is not a float'
        raise ParameterError(PARAMETER_TYPE, arg=a, msg=error)
    return arg


class BaseOptionsHandler:
    options_type = None

    def process_options(self, func: FunctionType, options):
        """
        Process parameters and return a list or dict

        :param func: The command method
        :param options: Parameter container specified by `options_type`
        """
        raise NotImplementedError


class SimpleOptionsHandler(BaseOptionsHandler):
    """ A simple parameters handler """
    options_type = 'Queue'

    @staticmethod
    def validate_options(func: FunctionType, options: Queue, args: list):
        annotation = func.__annotations__

        al = []
        for a in args:
            arg_type = annotation.get(a)
            if is_input(arg_type):
                if isinstance(arg_type, type):
                    arg_type = arg_type()

                if not arg_type.prompt:
                    arg_type.prompt = a

                default = func.__kwdefaults__.get(a) if func.__kwdefaults__ else None
                if default:
                    arg_type.default = default
                arg = arg_type.input()

                al.append(arg)
                continue

            try:
                arg = options.get(False)
            except Empty:
                break

            if arg_type == int:
                arg = assert_int(arg)
            elif arg_type == float:
                arg = assert_float(arg)

            al.append(arg)

        options.full()
        for i in al:
            options.put(i)

    def process_options(self, func: FunctionType, options: Queue) -> Union[list, dict, None]:
        args_count = func.__code__.co_argcount
        if 'args' in func.__code__.co_varnames:
            args_count += 1
        # pop up self & variables.
        args = list(func.__code__.co_varnames[1: args_count])

        if func.__kwdefaults__:
            for k in func.__kwdefaults__.keys():
                args.append(k)

        if not args:
            return

        if 'args' in args:
            res = []
            while True:
                try:
                    res.append(options.get(False))
                except Empty:
                    break
        else:
            self.validate_options(func, options, args)

            res = {}
            for arg in args:
                try:
                    res[arg] = options.get(False)
                except Empty:
                    if func.__defaults__:
                        if len(func.__defaults__) == len(args):
                            break
                    elif func.__kwdefaults__:
                        if arg in func.__kwdefaults__:
                            break
                    else:
                        raise ParameterError(MISS_PARAMETER, arg=arg)
        return res


class OptionsTagHandler(BaseOptionsHandler):
    options_type = 'list'

    @staticmethod
    def process_context(func):
        annotation = func.__annotations__

        tag_model_context = {}
        for arg, t in annotation.items():
            if is_options(t):
                t.arg = arg
                tag_model_context[arg] = {
                    'arglen': t.arglen,
                    'tag': t.tag,
                    'common_tag': t.common_tag,
                }

        tag_context = opt_set.get(func.__name__)
        if tag_context:
            tag_context.update(tag_model_context)
        else:
            tag_context = tag_model_context

        tmp_tag_context = copy.deepcopy(tag_context)

        tag_list = []
        if tag_context:
            for k, v in tmp_tag_context.items():
                if isinstance(v['tag'], str):
                    if v['tag'] in tag_list:
                        msg = f'Duplicate tag: {v["tag"]}'
                        raise DefinitionError(msg)

                    tag_list.append(v['tag'])
                elif isinstance(v['tag'], (tuple, list)):
                    for i in v['tag']:
                        if i in tag_list:
                            msg = f'Duplicate tag: {i}'
                            raise DefinitionError(msg)

                        tag_list.append(v['tag'])

                tag_context[k]['required'] = True
                if func.__kwdefaults__ and k in func.__kwdefaults__:
                    tag_context[k]['required'] = False

                if func.__annotations__.get(k) is not None and is_input(func.__annotations__[k]):
                    msg = 'Parameter decorated by `Options` cannot be defined as `Input` parameter'
                    raise DefinitionError(msg)
        return tag_context

    @staticmethod
    def validate_type(func, args: dict):
        annotation = func.__annotations__
        result = {}

        for k, v in args.items():
            arg_type = annotation.get(k)
            arg = v

            if is_input(arg_type):
                if isinstance(arg_type, type):
                    arg_type = arg_type()

                if not arg_type.prompt:
                    arg_type.prompt = k

                default = func.__kwdefaults__.get(k) if func.__kwdefaults__ else None
                if default:
                    arg_type.default = default
                arg = arg_type.input()

                result[k] = arg
                continue

            if isinstance(v, str):
                if arg_type == int:
                    arg = assert_int(v)
                elif arg_type == float:
                    arg = assert_float(v)

            elif isinstance(v, list):
                arg = []
                for i in v:
                    if arg_type == int:
                        i = assert_int(i)
                    elif arg_type == float:
                        i = assert_float(i)
                    arg.append(i)

            result[k] = arg
        return result

    def get_positional_parameters(self, context, opts, func):
        args_count = func.__code__.co_argcount
        if func.__kwdefaults__:
            args_count += len(func.__kwdefaults__)

        varnames = list(func.__code__.co_varnames[1: args_count])

        for key in context.keys():
            varnames.remove(key)

        pos_args = []
        for p in opts:
            if self.find_tag(p, context):
                break
            pos_args.append(p)

        args = {}

        for i in varnames[:]:
            var_type = func.__annotations__.get(i)
            if var_type and is_input(var_type):
                args[i] = None
                varnames.remove(i)

        for index, var in enumerate(varnames):
            try:
                args[var] = pos_args[index]
            except IndexError:
                raise ParameterError(MISS_PARAMETER, arg=var)
        return args

    def get_tag_parameters(self, context, opts):
        tag_args = {}
        tmp_context = context.copy()
        for k, v in context.items():
            tag = v['tag']
            index = None
            if isinstance(tag, str):
                if tag in opts:
                    index = opts.index(tag)
            elif isinstance(tag, (tuple, list)):
                for t in tag:
                    if t in opts:
                        index = opts.index(t)

            if index is None:
                if v.get('required', False) is False:
                    continue
                else:
                    raise ParameterError(MISS_PARAMETER, arg=k)

            params = []
            for p in opts[index + 1:]:
                if self.find_tag(p, tmp_context):
                    break
                params.append(p)

            tag_args[k] = params
        return tag_args

    @staticmethod
    def find_tag(p, context):
        found = False
        for ctx in context.values():
            tag = ctx['tag']
            if isinstance(tag, str):
                if p == tag:
                    found = True
                    break
            elif isinstance(tag, (tuple, list)):
                if p in tag:
                    found = True
                    break
        return found

    @staticmethod
    def validate_tag_parameters(tags, context):
        args = {}
        for k, v in context.items():
            tag_args_list = tags.get(k)

            if tag_args_list:
                s = ''
                if len(tag_args_list) > v['arglen']:
                    if v['arglen'] > 1:
                        s = 's'

                    msg = f'"{k}" takes {v["arglen"]} parameter{s} but {len(tag_args_list)} were given'
                    raise DefinitionError(msg)
                elif len(tag_args_list) < v['arglen']:
                    if v["arglen"] - len(tag_args_list):
                        s = 's'

                    msg = f'"{k}"[{v["common_tag"]}] missing {v["arglen"] - len(tag_args_list)} required parameter{s}'
                    raise DefinitionError(msg)
                else:
                    if len(tag_args_list) == 1:
                        args[k] = tag_args_list[0]
                    else:
                        args[k] = tag_args_list.copy()
            else:
                if v['required']:
                    raise ParameterError(MISS_PARAMETER, arg=k)
        return args

    def process_options(self, func: FunctionType, options: List[str]) -> dict:
        args_count = func.__code__.co_argcount
        if func.__kwdefaults__:
            args_count += len(func.__kwdefaults__)

        if args_count != len(func.__code__.co_varnames):
            msg = 'Parameters after `*` need to define default value'
            raise DefinitionError(msg)

        context = self.process_context(func)

        has_tag = False
        for var in func.__code__.co_varnames[1: args_count]:
            found = False if not context.get(var) else True
            arg_type = func.__annotations__.get(var)
            if found is False:
                if is_input(arg_type):
                    continue

                if has_tag:
                    msg = 'Cannot define positional parameter after parameter decorated by `Options`.'
                    raise DefinitionError(msg)
            else:
                has_tag = found

        pos_args = self.get_positional_parameters(context, options, func)
        tag_args = self.get_tag_parameters(context, options)
        args = self.validate_tag_parameters(tag_args, context)

        args.update(pos_args)
        args = self.validate_type(func, args)

        return args
