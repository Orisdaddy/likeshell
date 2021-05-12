from .context import alias_set, ignore_set
from functools import wraps


def alias(name: str):
    def i(func):
        @wraps(func)
        def set_alias(*args, **kwargs):
            func(*args, **kwargs)

        alias_set.add(name, func.__name__)
        return set_alias
    return i


def ignore(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        func(*args, **kwargs)

    ignore_set.add(func.__name__)
    return decorator

