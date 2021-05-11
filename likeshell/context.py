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
            raise RuntimeError(f'The aliases of "{af}" and "{f}" are duplicated')
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
