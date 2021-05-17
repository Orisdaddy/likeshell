import sys
import os
import difflib
from queue import Queue

from .console import *
from .comment import parse_comment
from .context import alias_set, ignore_set, opt_set
from .options import OptionsTagHandler, SimpleOptionsHandler
from .types import Options
from .exceptions import CommandError, COMMAND_NOT_FOUND

from typing import Optional


__BUILT_IN__ = ('__options_handler__', '__default_bash__')


class CommandHandler:
    def __init__(self, args, cls):
        self.args = args
        self.options = None

        self.tasks = cls()

        # if args is empty.
        if self.args:
            self.action = self.args[0]
        else:
            self.help()

    def load_parameters(self, func):
        if isinstance(self.tasks.__options_handler__, SimpleOptionsHandler):
            for t in func.__annotations__.values():
                if issubclass(t, Options):
                    self.tasks.__options_handler__ = OptionsTagHandler()
                    break

            if not opt_set.empty and opt_set.get(func.__name__):
                self.tasks.__options_handler__ = OptionsTagHandler()

        if self.tasks.__options_handler__.options_type == 'Queue':
            options = Queue()
            for a in self.args[1:]:
                options.put(a)
        else:
            options = self.args[1:]
        self.options = options

    def command_not_found(self, action, throws=True):
        instruction = {}
        instruction.update(alias_set.context)
        instruction.update(self.tasks.__ls_task__)

        similarity_dice = {}
        for i in instruction:
            qr = difflib.SequenceMatcher(a=action, b=i).quick_ratio()
            if qr:
                similarity_dice[i] = qr

        similarity = None
        if similarity_dice:
            similarity = max(similarity_dice, key=lambda k: similarity_dice[k])

        similar = ''
        if similarity:
            similar = f' Similar command: {similarity}'

        msg = f'Commend "{action}" is not found.{similar}'
        if throws:
            raise CommandError(COMMAND_NOT_FOUND, cmd=action, msg=msg)
        else:
            output(msg)

    def default_command(self):
        """
        If the command is not found in program,
        the command will be executed by the program specified by `__default_bash__`
        """
        if self.tasks.__default_bash__:
            cmd = ' '.join(self.args[1:])
            os.system(f'{self.tasks.__default_bash__} {cmd}')
        else:
            self.command_not_found(self.action)

    def run_script(self):
        action = self.action

        if ignore_set.exist(action) or action.startswith('_'):
            return self.command_not_found(self.action)

        if action in ('-h', '--help'):
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
            return self.command_not_found(self.action)

        self.load_parameters(func)

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
                    output_comment(task.__doc__, color=Color.GREEN)
                else:
                    output('The command description is empty.')
            else:
                self.command_not_found(self.action, False)
        else:
            output('帮助:')
            output('  <shell> -h')
            output('  <shell> -h <action>')
            output('用法:')
            output('  <shell> <action> [options...]', end='\n\n')

            cm = sorted(self.tasks.__ls_task__)
            output('命令:')
            for k in cm:
                # func_name = self.tasks.__ls_task__[k]
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

    cls.__ls_task__ = tasks
    ch = CommandHandler(args, cls)
    ch.run_script()


class GsMeta(type):
    def __init__(cls, what, ex, dic):
        if what != 'Shell':
            run_cls(cls, dic)
        super().__init__(what, ex, dic)


class Main:
    __options_handler__ = SimpleOptionsHandler()
    __default_bash__: str = None

    def __before__(self):
        pass

    def __after__(self):
        pass


class Shell(Main, metaclass=GsMeta):
    pass
