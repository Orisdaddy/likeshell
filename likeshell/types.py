import getpass

from types import FunctionType
from typing import Union
from .context import opt_set
from .exceptions import DefinitionError
from .typehints import OptStr, OptList


def adapt_colon(msg):
    if not isinstance(msg, str):
        return

    if not msg.endswith(':'):
        msg += ':'
    return msg


class Input:
    """
    Input
    """
    def __init__(self, prompt, default=None):
        self.prompt = prompt
        self.default = default
        self.msg = None

    def input(
            self,
            message: str = None,
            callback: FunctionType = None,
            hide: bool = False,
            default=None
    ):
        """
        Get input message.

        :param message: The prompt string
        :param callback: Requires receive 1 parameter and return 1 parameter
        :param hide: echo turned off, Used for a password
        """
        message = message or adapt_colon(self.prompt)
        default = default or self.default

        if hide is True:
            result = getpass.getpass(message)
        else:
            result = input(message)

        if not result and default is not None:
            result = default

        if callable(callback):
            result = callback(result)

        return result


class Options(OptList, OptStr):
    tag: Union[str, list] = None
    arglen: int = 1

    def __init__(
            self,
            arg: str,
            tag: Union[str, list, tuple] = None,
            arglen: int = 1
    ):
        if not tag:
            raise DefinitionError('"tag" cannot be empty')

        self.tag = tag
        self.arglen = arglen
        self.arg = arg

        if isinstance(tag, str):
            self.common_tag = tag
        elif isinstance(tag, (tuple, list)) and tag:
            self.common_tag = tag[0]
        else:
            self.common_tag = str(tag)

    def set_tag(self, func, tag):
        tag_context = {
            'arglen': self.arglen,
            'tag': tag,
            'common_tag': self.common_tag,
        }

        opt_set.add(func, self.arg, tag_context)
        return func

    def __call__(self, func):
        if isinstance(self.tag, (str, list, tuple)):
            self.set_tag(func.__name__, self.tag)
        else:
            tag = str(self.tag)
            self.set_tag(func.__name__, tag)
        return func


class Enumerate:
    pass


TYPES = (Input, Options, )

