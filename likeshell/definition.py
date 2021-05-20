import copy

from .exceptions import DefinitionError
from .types import Input, Options
from .context import opt_set


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


def check_definition(func):
    args_count = func.__code__.co_argcount
    if func.__kwdefaults__:
        args_count += len(func.__kwdefaults__)

    if args_count != len(func.__code__.co_varnames):
        msg = 'Parameters after `*` need to define default value'
        raise DefinitionError(msg)

    context = process_context(func)

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

    return context


def process_context(func):
    annotation = func.__annotations__

    tag_type_context = {}
    for arg, t in annotation.items():
        if is_options(t):
            t.arg = arg
            tag_type_context[arg] = {
                'arglen': t.arglen,
                'tag': t.tag,
                'common_tag': t.common_tag,
            }

    tag_context = opt_set.get(func.__name__)
    if tag_context:
        tag_context.update(tag_type_context)
    else:
        tag_context = tag_type_context

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

