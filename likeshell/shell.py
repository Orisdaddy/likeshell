import sys
import os
from queue import Queue
from .console import *
from .comment import parse_comment
from .context import alias_set, ignore_set

from typing import Optional


__BUILT_IN__ = ('__options_handler__', '__default_bash__')


def command_not_found(action, throws=True):
    msg = f'{action} is not found.'
    if throws:
        raise RuntimeError(msg)
    else:
        output(msg)


class CommandHandler:
    def __init__(self, args, cls):

        self.args = args

        self.tasks = cls()

        if self.tasks.__options_handler__.options_type == 'Queue':
            options = Queue()
            for a in args[1:]:
                options.put(a)
        else:
            options = args[1:]

        self.options = options

        if self.args:
            self.action = self.args[0]
        else:
            self.help()

    def default_command(self):
        """
        If the command is not found in program,
        the command will be executed by the program specified by `__default_bash__`
        """
        if self.tasks.__default_bash__:
            cmd = ' '.join(self.args[1:])
            os.system(f'{self.tasks.__default_bash__} {cmd}')
        else:
            command_not_found(self.action)

    def run_script(self):
        action = self.action

        if ignore_set.exist(action) or action.startswith('_'):
            return command_not_found(self.action)

        if action == '-h':
            if len(self.args) > 1:
                option = self.args[1]
            else:
                option = None
            self.help(option)

        if not alias_set.empty:
            if alias_set.get(action):
                action = alias_set.get(action)

                if ignore_set.exist(action):
                    return

        func = getattr(self.tasks, action, None)

        if func is None:
            self.default_command()

        if not callable(func):
            return command_not_found(self.action)

        if isinstance(self.tasks.__options_handler__, type):
            args = self.tasks.__options_handler__().process_options(func, self.options)
        else:
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
                command_not_found(self.action, False)
        else:
            output('帮助:')
            output('  <shell> -h')
            output('  <shell> -h <action>')
            output('用法:')
            output('  <shell> <action> [options...]', end='\n\n')

            cm = sorted(self.tasks.__likeshell_task__)
            output('命令:')
            for k in cm:
                # func_name = self.tasks.__likeshell_task__[k]
                space = ' '
                opt = f'  {k}'
                output(opt)
        sys.exit()


def run_cls(cls, dic):
    args = sys.argv[1:]
    tasks = {
        k: v for k, v in dic.items()
        if not (k.startswith('_') or k.endswith('__')) and k not in __BUILT_IN__ and not ignore_set.exist(k)
    }

    for k, v in tasks.items():
        if v.__doc__:
            doc_meta = parse_comment(v.__doc__)
            alias = doc_meta.get('alias')
            if alias:
                alias_set.add(alias, v.__name__)

    cls.__likeshell_task__ = tasks
    ch = CommandHandler(args, cls)
    ch.run_script()


class GsMeta(type):
    def __init__(cls, what, ex, dic):
        if what != 'Shell':
            run_cls(cls, dic)
        super().__init__(what, ex, dic)
