import sys
import os
from queue import Queue
from .console import *
from .comment import parse_comment
from .context import alias_set

from typing import Optional


__BUILT_IN__ = ('__options_handler__', '__default_bash__')


class CommandHandler:
    def __init__(self, args, cls):

        self.args = args

        options = Queue()
        for a in args[1:]:
            options.put(a)
        self.options = options

        self.tasks = cls()
        if self.args:
            self.action = self.args[0]
        else:
            self.help()

    def default_command(self):
        if self.tasks.__default_bash__:
            cmd = ' '.join(self.args[1:])
            os.system(f'{self.tasks.__default_bash__} {cmd}')

    def run_script(self):
        action = self.action
        if action == '-h':
            if len(self.args) > 1:
                option = self.args[1]
            else:
                option = None
            self.help(option)

        if not alias_set.empty:
            if alias_set.get(action):
                action = alias_set.get(action)

        func = getattr(self.tasks, action, None)

        if func is None:
            self.default_command()

        if not callable(func):
            return

        args = self.tasks.__options_handler__.process_options(func, self.options)

        self.tasks.__before__()

        # run task
        if isinstance(args, dict):
            func(**args)
        elif isinstance(args, list):
            func(*args)
        else:
            func()

        self.tasks.__after__()

    def help(self, option: Optional[str] = None):
        if option:
            if not alias_set.empty:
                if alias_set.get(option):
                    option = alias_set.get(option)

            task = getattr(self.tasks, option, None)
            if task:
                if task.__doc__:
                    output_comment(task.__doc__, color=GREEN)
                else:
                    output('The command description is empty.')
            else:
                output('The command is not fount.')
        else:
            output('帮助:')
            output('  <shell> -h')
            output('  <shell> -h <action>')
            output('用法:')
            output('  <shell> <action> [options...]', end='\n\n')

            cm = sorted(self.tasks.__task__)
            output('命令:')
            for k in cm:
                # func_name = self.tasks.__task__[k]
                space = ' '
                opt = f'  {k}'
                output(opt)
        sys.exit()


def run_cls(cls, dic):
    args = sys.argv[1:]
    tasks = {
        k: v for k, v in dic.items()
        if not (k.startswith('_') or k.endswith('__') and k not in __BUILT_IN__)
    }

    for k, v in tasks.items():
        if v.__doc__:
            doc_meta = parse_comment(v.__doc__)
            alias = doc_meta.get('alias')
            alias_set.add(alias, v.__name__)

    cls.__task__ = tasks
    ch = CommandHandler(args, cls)
    ch.run_script()


class GsMeta(type):
    def __init__(cls, what, ex, dic):
        if what != 'Shell':
            run_cls(cls, dic)
        super().__init__(what, ex, dic)
