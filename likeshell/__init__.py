from .shell import GsMeta
from .options import SimpleOptionsHandler
from .decoration import alias, ignore
from .types import Input


class Main:
    __options_handler__ = SimpleOptionsHandler()
    __default_bash__: str = None

    def __before__(self):
        pass

    def __after__(self):
        pass


class Shell(Main, metaclass=GsMeta):
    pass
