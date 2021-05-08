from .shell import GsMeta
from .options import SimpleOptionsHandler


class Shell(metaclass=GsMeta):
    options_handler = SimpleOptionsHandler()

