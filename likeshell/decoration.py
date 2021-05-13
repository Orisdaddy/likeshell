from .context import alias_set, ignore_set


def alias(name: str):
    def decorator(func):
        alias_set.add(name, func.__name__)
        return func
    return decorator


def ignore(func):
    ignore_set.add(func.__name__)
    return func

