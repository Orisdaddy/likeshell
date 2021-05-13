import getpass

from types import FunctionType
from typing import Union


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
    def __init__(self, args):
        self.default = args
        self.msg = None

    def input(
            self,
            message: str = None,
            callback: FunctionType = None,
            hide: bool = False
    ):
        """
        Get input message.

        :param message: The prompt string
        :param callback: Requires receive 1 parameter and return 1 parameter
        :param hide: echo turned off, Used for a password
        """
        message = message or adapt_colon(self.default)

        if hide is True:
            result = getpass.getpass(message)
        else:
            result = input(message)

        if callable(callback):
            result = callback(result)
        return result


class Options:
    tag: Union[str, list] = None
    arglen: int = None

    def __init__(
            self,
            arg: str,
            tag: Union[str, list, tuple] = None,
            arglen: int = 1
    ):
        if not tag:
            raise RuntimeError('"tag" cannot be empty')

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
            self.arg: {
                'arglen': self.arglen,
                'tag': tag,
                'common_tag': self.common_tag,
            }
        }
        setattr(func, '__ls_tag__', tag_context)
        return func

    def __call__(self, func):
        if isinstance(self.tag, (str, list, tuple)):
            self.set_tag(func, self.tag)
        else:
            tag = str(self.tag)
            self.set_tag(func, tag)
        return func


class Enumerate:
    pass


TYPES = (Input, Options, )

