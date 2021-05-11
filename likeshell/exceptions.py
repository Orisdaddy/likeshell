PARAMETER_TYPE = 'TypeError'
MISS_PARAMETER = 'MissingParameter'


class LikeShellError(Exception):
    pass


class ParameterError(LikeShellError):
    pass


class UsageError(LikeShellError):
    pass
