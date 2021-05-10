from .shell import GsMeta
from .options import SimpleOptionsHandler


class Shell(metaclass=GsMeta):
    options_handler = SimpleOptionsHandler()
    default_bash = None

    def __after(self):
        pass
