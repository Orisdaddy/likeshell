class Alias:
    def __init__(self):
        self.namespace = {}

    def add_alias(self, name, f):
        af = self.get_alias(name)
        if af and af != f:
            raise RuntimeError(f'The aliases of "{af}" and "{f}" are duplicated')
        self.namespace[name] = f

    def pop_alias(self, name):
        return self.namespace.pop(name)

    def get_alias(self, name):
        return self.namespace.get(name)


alias_set = Alias()
