import getpass

from types import FunctionType


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


class Enumerate:
    pass


class Options:
    pass


TYPES = (Input,)

