from .shell import GsMeta
from .options import SimpleOptionsHandler


class Shell(metaclass=GsMeta):
    __options_handler__ = SimpleOptionsHandler()
    __default_bash__ = None

    def __before__(self):
        pass

    def __after__(self):
        pass
