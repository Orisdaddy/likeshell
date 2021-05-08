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
        for a in args:
            arg = options.get(False)
            arg_type = annotation.get(a)

            if arg_type == int:
                if arg.isdigit():
                    arg = int(arg)
                else:
                    error = f'参数<{a}> 得到值"{arg}" 无法解析为int'
                    raise TypeError(error)

            if arg_type == float:
                try:
                    arg = float(arg)
                except ValueError:
                    error = f'参数<{a}> 得到值"{arg}" 无法解析为float'
                    raise TypeError(error)

            al.append(arg)

            if options.empty():
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

        self.validate_options(func, options, args)

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
                        raise NotImplementedError(f'缺少参数"{arg}"')
        return res
