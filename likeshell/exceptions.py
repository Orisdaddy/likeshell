PARAMETER_TYPE = 'TypeError'
MISS_PARAMETER = 'MissingParameter'


class LikeShellError(Exception):
    pass


class UsageError(LikeShellError):
    pass


class DefinitionError(LikeShellError):
    pass


class ParameterError(LikeShellError):
    pass

