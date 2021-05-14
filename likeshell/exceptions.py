PARAMETER_TYPE = 'ParameterTypeError'
MISS_PARAMETER = 'MissingParameter'
COMMAND_NOT_FOUND = 'CommandNotFound'


class LikeShellError(Exception):
    pass


class UsageError(LikeShellError):
    pass


class DefinitionError(LikeShellError):
    pass


class CommandError(LikeShellError):
    def __init__(self, code, cmd, msg=None):
        self.code = code
        self.cmd = cmd
        self.message = msg

    def __str__(self):
        return f'{self.code}: {self.message}'


class ParameterError(LikeShellError):
    def __init__(self, code, arg, msg=None):
        self.code = code
        self.arg = arg
        self.message = msg

    def __str__(self):
        if self.code == MISS_PARAMETER:
            return f'{self.code}: {self.arg}.'
        else:
            return f'{self.code}: {self.message}'
