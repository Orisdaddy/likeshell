import copy

from queue import Queue, Empty

from types import FunctionType
from typing import Union, List

from .types import Input, Options


SKIP_GETVALUE = ('Input', )


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

            if hasattr(arg_type, '__name__') and arg_type.__name__ in SKIP_GETVALUE:
                arg = None
                if arg_type.__name__ == 'Input':
                    arg = Input(args)

                al.append(arg)
                continue

            try:
                arg = options.get(False)
            except Empty:
                break

            if arg_type == int:
                if arg.isdigit():
                    arg = int(arg)
                else:
                    error = f'"{arg}" is not a int'
                    raise TypeError(error)

            if arg_type == float:
                try:
                    arg = float(arg)
                except ValueError:
                    error = f'"{arg}" is not a float'
                    raise TypeError(error)

            al.append(arg)

            if options.empty():
                break

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
                        msg = f'Missing parameter "{arg}"'
                        raise ValueError(msg)
        return res


class OptionsTagHandler(BaseOptionsHandler):
    options_type = 'list'

    @staticmethod
    def process_context(func):
        annotation = func.__annotations__

        tag_model_context = {}
        for arg, t in annotation.items():
            if issubclass(t, Options):
                if isinstance(t.tag, str):
                    common_tag = t.tag
                elif isinstance(t.tag, (tuple, list)) and t.tag:
                    common_tag = t.tag[0]
                else:
                    common_tag = str(t.tag)

                tag_model_context[arg] = {
                    'arglen': t.arglen,
                    'tag': t.tag,
                    'common_tag': common_tag,
                }

        tag_context = getattr(func, '__ls_tag__', None)

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
                        raise RuntimeError(msg)

                    tag_list.append(v['tag'])
                elif isinstance(v['tag'], (tuple, list)):
                    for i in v['tag']:
                        if i in tag_list:
                            msg = f'Duplicate tag: {i}'
                            raise RuntimeError(msg)

                        tag_list.append(v['tag'])

                tag_context[k]['required'] = True

                if func.__kwdefaults__ and k in func.__kwdefaults__:
                    tag_context[k]['required'] = False
        return tag_context

    def get_positional_parameters(self, context, opts, func):
        varnames = list(func.__code__.co_varnames[1:])
        for key in context.keys():
            varnames.remove(key)

        pos_args = []
        for p in opts:
            if self.find_tag(p, context):
                break
            pos_args.append(p)

        args = {}
        for index, var in enumerate(varnames):
            try:
                args[var] = pos_args[index]
            except IndexError:
                raise RuntimeError(f'Miss parameter {var}')
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
                    raise RuntimeError(msg)
                elif len(tag_args_list) < v['arglen']:
                    if v["arglen"] - len(tag_args_list):
                        s = 's'

                    msg = f'"{k}"[{v["common_tag"]}] missing {v["arglen"] - len(tag_args_list)} required parameter{s}'
                    raise RuntimeError(msg)
                else:
                    args[k] = tag_args_list.copy()
            else:
                if v['required']:
                    msg = f'Missing parameter "{k}"'
                    raise RuntimeError(msg)
        return args

    def process_options(self, func: FunctionType, options: List[str]) -> dict:
        context = self.process_context(func)

        pos_args = self.get_positional_parameters(context, options, func)
        tag_args = self.get_tag_parameters(context, options)
        args = self.validate_tag_parameters(tag_args, context)

        args.update(pos_args)

        has_tag = False
        for var in func.__code__.co_varnames[1:]:
            if var not in args:
                if has_tag:
                    msg = 'Cannot define positional parameter after parameter decorated by `Options`.'
                    raise RuntimeError(msg)
            else:
                has_tag = True

        return args
