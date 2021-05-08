from queue import Queue, Empty

from types import FunctionType
from typing import Union


class BaseOptionsHandler:
    def process_options(self, func: FunctionType, options: Queue):
        raise NotImplementedError


class SimpleOptionsHandler(BaseOptionsHandler):
    """ 顺序解析器 """
    options_type = 'Queue'

    @staticmethod
    def validate_options(func: FunctionType, options: Queue, args: list):
        annotation = func.__annotations__
        al = []
        for i in range(1000):
            try:
                arg = options.get(False)
                arg_type = annotation[args[i]]

                if arg_type == int:
                    if not arg.isdigit():
                        raise TypeError(f'{args[i]} is not a number')
                    else:
                        arg = int(arg)
                al.append(arg)
            except Empty:
                break
        for i in al:
            options.put(i)

    def process_options(self, func: FunctionType, options: Queue) -> Union[list, dict, None]:

        args_count = func.__code__.co_argcount
        if 'args' in func.__code__.co_varnames:
            args_count += 1
        # pop up self & variables.
        args = list(func.__code__.co_varnames[1: args_count])
        if func.__kwdefaults__:
            for k in func.__kwdefaults__.keys():
                args.append(k)

        if not args:
            return

        # self.validate_options(func, options, args)

        if 'args' in args:
            res = []
            while True:
                try:
                    res.append(options.get(False))
                except Empty:
                    break
        else:
            res = {}
            for arg in args:
                try:
                    res[arg] = options.get(False)
                except Empty:
                    if func.__defaults__:
                        if len(func.__defaults__) == len(args):
                            break
                    elif func.__kwdefaults__:
                        if arg in func.__kwdefaults__:
                            break
                    else:
                        raise NotImplementedError(f'Miss {arg}')
        return res
