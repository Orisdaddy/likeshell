from .exceptions import DefinitionError


class Context:
    def __init__(self, context=None):
        if context is None:
            self.context = {}
        else:
            self.context = context

    @property
    def empty(self):
        return not self.context


class Alias(Context):
    def add(self, name, f):
        af = self.get(name)
        if af and af != f:
            msg = f'The aliases of "{af}" and "{f}" are duplicated'
            raise DefinitionError(msg)
        self.context[name] = f

    def pop(self, name):
        return self.context.pop(name)

    def get(self, name):
        return self.context.get(name)


alias_set = Alias()


class Argument(Context):
    def __init__(self, func_name):
        self.func_name = func_name
        super().__init__()

    def add(self, name, f):
        self.context[name] = f

    def pop(self, name):
        return self.context.pop(name)

    def get(self, name):
        return self.context.get(name)


class Ignore(Context):
    def __init__(self):
        super().__init__([])

    def add(self, name):
        self.context.append(name)

    def exist(self, name):
        return name in self.context


ignore_set = Ignore()


class Options(Context):
    def add(self, func, arg, ctx):
        if self.context.get(func):
            self.context[func][arg] = ctx
        else:
            self.context[func] = {arg: ctx}

    def get(self, func):
        return self.context.get(func)


opt_set = Options()
