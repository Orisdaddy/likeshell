import os

__OUTPUT_STR = '\033[{background};{color}m{content}\033[0m'
BOLD = 1
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37

BG_BOLD = 11
BG_BLACK = 40
BG_RED = 41
BG_GREEN = 42
BG_YELLOW = 43
BG_BLUE = 44
BG_MAGENTA = 45
BG_CYAN = 46
BG_WHITE = 47


def output(content, background=0, color=WHITE, *args, **kwargs):
    print(__OUTPUT_STR.format(
        background=background,
        color=color,
        content=content,
    ), *args, **kwargs)


def output_comment(content, background=0, color=WHITE, *args, **kwargs):
    msg = ''
    for i in content.split(os.linesep):
        msg += f'  {i.strip()}{os.linesep}'
    print(__OUTPUT_STR.format(
        background=background,
        color=color,
        content=msg,
    ), *args, **kwargs)
