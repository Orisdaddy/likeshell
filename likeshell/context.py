from .exceptions import DefinitionError


def empty_set():
    opt_set.full()
    alias_set.full()
    ignore_set.full([])


class Context:
    def __init__(self, context=None):
        if context is None:
            self.context = {}
        else:
            self.context = context

    def full(self, ctx=None):
        if ctx is not None:
            self.context = ctx
        else:
            self.context = {}

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

    def find_alias(self, name):
        for a, n in self.context.items():
            if n == name:
                return a


alias_set = Alias()


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


class Descriptions(Context):
    def add(self, name, desc):
        self.context[name] = desc

    def get(self, name):
        return self.context.get(name)


desc_set = Descriptions()
