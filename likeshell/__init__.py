from .shell import GsMeta
from .options import SimpleOptionsHandler
from .decoration import alias, ignore


class Main:
    __options_handler__ = SimpleOptionsHandler()
    __default_bash__ = None

    def __before__(self):
        pass

    def __after__(self):
        pass


class Shell(Main, metaclass=GsMeta):
    pass
