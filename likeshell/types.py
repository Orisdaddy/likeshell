import getpass

from types import FunctionType
from typing import Union
from .context import opt_set
from .exceptions import DefinitionError


class OptStr:
    """
    str(object='') -> str
    str(bytes_or_buffer[, encoding[, errors]]) -> str

    Create a new string object from the given object. If encoding or
    errors is specified, then the object must expose a data buffer
    that will be decoded using the given encoding and error handler.
    Otherwise, returns the result of object.__str__() (if defined)
    or repr(object).
    encoding defaults to sys.getdefaultencoding().
    errors defaults to 'strict'.
    """

    def capitalize(self):
        """
        S.capitalize() -> str

        Return a capitalized version of S, i.e. make the first character
        have upper case and the rest lower case.
        """
        return ""

    def casefold(self):
        """
        S.casefold() -> str

        Return a version of S suitable for caseless comparisons.
        """
        return ""

    def center(self, width, fillchar=None):
        """
        S.center(width[, fillchar]) -> str

        Return S centered in a string of length width. Padding is
        done using the specified fill character (default is a space)
        """
        return ""

    def count(self, sub, start=None, end=None):
        """
        S.count(sub[, start[, end]]) -> int

        Return the number of non-overlapping occurrences of substring sub in
        string S[start:end].  Optional arguments start and end are
        interpreted as in slice notation.
        """
        return 0

    def encode(self, encoding='utf-8', errors='strict'):
        """
        S.encode(encoding='utf-8', errors='strict') -> bytes

        Encode S using the codec registered for encoding. Default encoding
        is 'utf-8'. errors may be given to set a different error
        handling scheme. Default is 'strict' meaning that encoding errors raise
        a UnicodeEncodeError. Other possible values are 'ignore', 'replace' and
        'xmlcharrefreplace' as well as any other name registered with
        codecs.register_error that can handle UnicodeEncodeErrors.
        """
        return b""

    def endswith(self, suffix, start=None, end=None):
        """
        S.endswith(suffix[, start[, end]]) -> bool

        Return True if S ends with the specified suffix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        suffix can also be a tuple of strings to try.
        """
        return False

    def expandtabs(self, tabsize=8):
        """
        S.expandtabs(tabsize=8) -> str

        Return a copy of S where all tab characters are expanded using spaces.
        If tabsize is not given, a tab size of 8 characters is assumed.
        """
        return ""

    def find(self, sub, start=None, end=None):
        """
        S.find(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        """
        return 0

    def format(self, *args, **kwargs):
        """
        S.format(*args, **kwargs) -> str

        Return a formatted version of S, using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').
        """
        pass

    def format_map(self, mapping):
        """
        S.format_map(mapping) -> str

        Return a formatted version of S, using substitutions from mapping.
        The substitutions are identified by braces ('{' and '}').
        """
        return ""

    def index(self, sub, start=None, end=None):
        """
        S.index(sub[, start[, end]]) -> int

        Return the lowest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        """
        return 0

    def isalnum(self):
        """
        S.isalnum() -> bool

        Return True if all characters in S are alphanumeric
        and there is at least one character in S, False otherwise.
        """
        return False

    def isalpha(self):
        """
        S.isalpha() -> bool

        Return True if all characters in S are alphabetic
        and there is at least one character in S, False otherwise.
        """
        return False

    def isdecimal(self):
        """
        S.isdecimal() -> bool

        Return True if there are only decimal characters in S,
        False otherwise.
        """
        return False

    def isdigit(self):
        """
        S.isdigit() -> bool

        Return True if all characters in S are digits
        and there is at least one character in S, False otherwise.
        """
        return False

    def isidentifier(self):
        """
        S.isidentifier() -> bool

        Return True if S is a valid identifier according
        to the language definition.

        Use keyword.iskeyword() to test for reserved identifiers
        such as "def" and "class".
        """
        return False

    def islower(self):
        """
        S.islower() -> bool

        Return True if all cased characters in S are lowercase and there is
        at least one cased character in S, False otherwise.
        """
        return False

    def isnumeric(self):
        """
        S.isnumeric() -> bool

        Return True if there are only numeric characters in S,
        False otherwise.
        """
        return False

    def isprintable(self):
        """
        S.isprintable() -> bool

        Return True if all characters in S are considered
        printable in repr() or S is empty, False otherwise.
        """
        return False

    def isspace(self):
        """
        S.isspace() -> bool

        Return True if all characters in S are whitespace
        and there is at least one character in S, False otherwise.
        """
        return False

    def istitle(self):
        """
        S.istitle() -> bool

        Return True if S is a titlecased string and there is at least one
        character in S, i.e. upper- and titlecase characters may only
        follow uncased characters and lowercase characters only cased ones.
        Return False otherwise.
        """
        return False

    def isupper(self):
        """
        S.isupper() -> bool

        Return True if all cased characters in S are uppercase and there is
        at least one cased character in S, False otherwise.
        """
        return False

    def join(self, iterable):
        """
        S.join(iterable) -> str

        Return a string which is the concatenation of the strings in the
        iterable.  The separator between elements is S.
        """
        return ""

    def ljust(self, width, fillchar=None):
        """
        S.ljust(width[, fillchar]) -> str

        Return S left-justified in a Unicode string of length width. Padding is
        done using the specified fill character (default is a space).
        """
        return ""

    def lower(self):
        """
        S.lower() -> str

        Return a copy of the string S converted to lowercase.
        """
        return ""

    def lstrip(self, chars=None):
        """
        S.lstrip([chars]) -> str

        Return a copy of the string S with leading whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        """
        return ""

    def maketrans(self, *args, **kwargs):
        """
        Return a translation table usable for str.translate().

        If there is only one argument, it must be a dictionary mapping Unicode
        ordinals (integers) or characters to Unicode ordinals, strings or None.
        Character keys will be then converted to ordinals.
        If there are two arguments, they must be strings of equal length, and
        in the resulting dictionary, each character in x will be mapped to the
        character at the same position in y. If there is a third argument, it
        must be a string, whose characters will be mapped to None in the result.
        """
        pass

    def partition(self, sep):
        """
        S.partition(sep) -> (head, sep, tail)

        Search for the separator sep in S, and return the part before it,
        the separator itself, and the part after it.  If the separator is not
        found, return S and two empty strings.
        """
        pass

    def replace(self, old, new, count=None):
        """
        S.replace(old, new[, count]) -> str

        Return a copy of S with all occurrences of substring
        old replaced by new.  If the optional argument count is
        given, only the first count occurrences are replaced.
        """
        return ""

    def rfind(self, sub, start=None, end=None):
        """
        S.rfind(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.
        """
        return 0

    def rindex(self, sub, start=None, end=None):
        """
        S.rindex(sub[, start[, end]]) -> int

        Return the highest index in S where substring sub is found,
        such that sub is contained within S[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.
        """
        return 0

    def rjust(self, width, fillchar=None):
        """
        S.rjust(width[, fillchar]) -> str

        Return S right-justified in a string of length width. Padding is
        done using the specified fill character (default is a space).
        """
        return ""

    def rpartition(self, sep):
        """
        S.rpartition(sep) -> (head, sep, tail)

        Search for the separator sep in S, starting at the end of S, and return
        the part before it, the separator itself, and the part after it.  If the
        separator is not found, return two empty strings and S.
        """
        pass

    def rsplit(self, sep=None, maxsplit=-1):
        """
        S.rsplit(sep=None, maxsplit=-1) -> list of strings

        Return a list of the words in S, using sep as the
        delimiter string, starting at the end of the string and
        working to the front.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified, any whitespace string
        is a separator.
        """
        return []

    def rstrip(self, chars=None):
        """
        S.rstrip([chars]) -> str

        Return a copy of the string S with trailing whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        """
        return ""

    def split(self, sep=None, maxsplit=-1):
        """
        S.split(sep=None, maxsplit=-1) -> list of strings

        Return a list of the words in S, using sep as the
        delimiter string.  If maxsplit is given, at most maxsplit
        splits are done. If sep is not specified or is None, any
        whitespace string is a separator and empty strings are
        removed from the result.
        """
        return []

    def splitlines(self, keepends=None):
        """
        S.splitlines([keepends]) -> list of strings

        Return a list of the lines in S, breaking at line boundaries.
        Line breaks are not included in the resulting list unless keepends
        is given and true.
        """
        return []

    def startswith(self, prefix, start=None, end=None):
        """
        S.startswith(prefix[, start[, end]]) -> bool

        Return True if S starts with the specified prefix, False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        prefix can also be a tuple of strings to try.
        """
        return False

    def strip(self, chars=None):
        """
        S.strip([chars]) -> str

        Return a copy of the string S with leading and trailing
        whitespace removed.
        If chars is given and not None, remove characters in chars instead.
        """
        return ""

    def swapcase(self):
        """
        S.swapcase() -> str

        Return a copy of S with uppercase characters converted to lowercase
        and vice versa.
        """
        return ""

    def title(self):
        """
        S.title() -> str

        Return a titlecased version of S, i.e. words start with title case
        characters, all remaining cased characters have lower case.
        """
        return ""

    def translate(self, table):
        """
        S.translate(table) -> str

        Return a copy of the string S in which each character has been mapped
        through the given translation table. The table must implement
        lookup/indexing via __getitem__, for instance a dictionary or list,
        mapping Unicode ordinals to Unicode ordinals, strings, or None. If
        this operation raises LookupError, the character is left untouched.
        Characters mapped to None are deleted.
        """
        return ""

    def upper(self):
        """
        S.upper() -> str

        Return a copy of S converted to uppercase.
        """
        return ""

    def zfill(self, width):
        """
        S.zfill(width) -> str

        Pad a numeric string S with zeros on the left, to fill a field
        of the specified width. The string S is never truncated.
        """
        return ""

    def __add__(self, *args, **kwargs):
        """ Return self+value. """
        pass

    def __contains__(self, *args, **kwargs):
        """ Return key in self. """
        pass

    def __eq__(self, *args, **kwargs):
        """ Return self==value. """
        pass

    def __format__(self, format_spec):
        """
        S.__format__(format_spec) -> str

        Return a formatted version of S as described by format_spec.
        """
        return ""

    def __getitem__(self, *args, **kwargs):
        """ Return self[key]. """
        pass

    def __getnewargs__(self, *args, **kwargs):
        pass

    def __ge__(self, *args, **kwargs):
        """ Return self>=value. """
        pass

    def __gt__(self, *args, **kwargs):
        """ Return self>value. """
        pass

    def __hash__(self, *args, **kwargs):
        """ Return hash(self). """
        pass

    def __iter__(self, *args, **kwargs):
        """ Implement iter(self). """
        pass

    def __len__(self, *args, **kwargs):
        """ Return len(self). """
        pass

    def __le__(self, *args, **kwargs):
        """ Return self<=value. """
        pass

    def __lt__(self, *args, **kwargs):
        """ Return self<value. """
        pass

    def __mod__(self, *args, **kwargs):
        """ Return self%value. """
        pass

    def __mul__(self, *args, **kwargs):
        """ Return self*value. """
        pass

    def __ne__(self, *args, **kwargs):
        """ Return self!=value. """
        pass

    def __repr__(self, *args, **kwargs):
        """ Return repr(self). """
        pass

    def __rmod__(self, *args, **kwargs):
        """ Return value%self. """
        pass

    def __rmul__(self, *args, **kwargs):
        """ Return value*self. """
        pass

    def __sizeof__(self):
        """ S.__sizeof__() -> size of S in memory, in bytes """
        pass

    def __str__(self, *args, **kwargs):
        """ Return str(self). """
        pass


class OptList:
    def append(self, p_object):
        """ L.append(object) -> None -- append object to end """
        pass

    def clear(self):
        """ L.clear() -> None -- remove all items from L """
        pass

    def copy(self):
        """ L.copy() -> list -- a shallow copy of L """
        return []

    def count(self, value):
        """ L.count(value) -> integer -- return number of occurrences of value """
        return 0

    def extend(self, iterable):
        """ L.extend(iterable) -> None -- extend list by appending elements from the iterable """
        pass

    def index(self, value, start: int = None, stop: int = None):
        """
        L.index(value, [start, [stop]]) -> integer -- return first index of value.
        Raises ValueError if the value is not present.
        """
        return 0

    def insert(self, index, p_object):
        """ L.insert(index, object) -- insert object before index """
        pass

    def pop(self, index=None):
        """
        L.pop([index]) -> item -- remove and return item at index (default last).
        Raises IndexError if list is empty or index is out of range.
        """
        pass

    def remove(self, value):
        """
        L.remove(value) -> None -- remove first occurrence of value.
        Raises ValueError if the value is not present.
        """
        pass

    def reverse(self):
        """ L.reverse() -- reverse *IN PLACE* """
        pass

    def sort(self, key=None, reverse=False):
        """ L.sort(key=None, reverse=False) -> None -- stable sort *IN PLACE* """
        pass

    def __add__(self, *args, **kwargs):
        """ Return self+value. """
        pass

    def __contains__(self, *args, **kwargs):
        """ Return key in self. """
        pass

    def __delitem__(self, *args, **kwargs):
        """ Delete self[key]. """
        pass

    def __eq__(self, *args, **kwargs):
        """ Return self==value. """
        pass

    def __getitem__(self, y):
        """ x.__getitem__(y) <==> x[y] """
        pass

    def __ge__(self, *args, **kwargs):
        """ Return self>=value. """
        pass

    def __gt__(self, *args, **kwargs):
        """ Return self>value. """
        pass

    def __iadd__(self, *args, **kwargs):
        """ Implement self+=value. """
        pass

    def __imul__(self, *args, **kwargs):
        """ Implement self*=value. """
        pass

    def __iter__(self, *args, **kwargs):
        """ Implement iter(self). """
        pass

    def __len__(self, *args, **kwargs):
        """ Return len(self). """
        pass

    def __le__(self, *args, **kwargs):
        """ Return self<=value. """
        pass

    def __lt__(self, *args, **kwargs):
        """ Return self<value. """
        pass

    def __mul__(self, *args, **kwargs):
        """ Return self*value. """
        pass

    def __ne__(self, *args, **kwargs):
        """ Return self!=value. """
        pass

    def __repr__(self, *args, **kwargs):
        """ Return repr(self). """
        pass

    def __reversed__(self):
        """ L.__reversed__() -- return a reverse iterator over the list """
        pass

    def __rmul__(self, *args, **kwargs):
        """ Return value*self. """
        pass

    def __setitem__(self, *args, **kwargs):
        """ Set self[key] to value. """
        pass

    def __sizeof__(self):
        """ L.__sizeof__() -- size of L in memory, in bytes """
        pass


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

