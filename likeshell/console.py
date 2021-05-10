__OUTPUT_STR = '\033[{weight};{color}m{content}\033[0m'
BOLD = 1
BLACK = 30
RED = 31
GREEN = 32
YELLOW = 33
BLUE = 34
MAGENTA = 35
CYAN = 36
WHITE = 37


def output(content, weight=0, color=37, *args, **kwargs):
    print(__OUTPUT_STR.format(
        weight=weight,
        color=color,
        content=content,
    ), *args, **kwargs)
