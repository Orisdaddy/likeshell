from .alias import alias_set
from functools import wraps


def alias(name):
    def i(func):
        @wraps(func)
        def set_alias(*args, **kwargs):
            func(*args, **kwargs)

        alias_set.add_alias(name, func.__name__)
        return set_alias
    return i