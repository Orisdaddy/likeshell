import sys
import os
import difflib
from queue import Queue

from .console import *
from .comment import parse_comment
from .context import alias_set, ignore_set, opt_set, desc_set
from .options import OptionsTagHandler, SimpleOptionsHandler
from .types import Options
from .exceptions import CommandError, COMMAND_NOT_FOUND
from .util import cmd, find_description
from .definition import check_definition

from typing import Optional


__BUILT_IN__ = ('__options_handler__', '__default_bash__')


class CommandHandler:
    def __init__(self, args, cls):
        self.args = args
        self.options = None

        self.tasks = cls()

        self.context_mapping = {}
        for k, f in self.tasks.__ls_task__.items():
            if isinstance(self.select_handler(f), OptionsTagHandler):
                self.context_mapping[k] = check_definition(f)

        # if args is empty.
        if self.args:
            self.action = self.args[0]
        else:
            self.help()

    def select_handler(self, func):
        if isinstance(self.tasks.__options_handler__, SimpleOptionsHandler):
            for t in func.__annotations__.values():
                if isinstance(t, Options):
                    return OptionsTagHandler()

            if not opt_set.empty and opt_set.get(func.__name__):
                return OptionsTagHandler()
        return SimpleOptionsHandler()

    def load_parameters(self, func):
        handler = self.select_handler(func)
        self.tasks.__options_handler__ = handler

        if self.tasks.__options_handler__.options_type == 'Queue':
            options = Queue()
            for a in self.args[1:]:
                options.put(a)
        else:
            options = self.args[1:]
        self.options = options

    def command_not_found(self, action, throws=True):
        instruction = {}
        instruction.update(self.tasks.__ls_task__)
        for v in alias_set.context.values():
            if v in self.tasks.__ls_task__:
                del instruction[v]
        instruction.update(alias_set.context)

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
            cmdarg = ' '.join(self.args)
            os.system(f'{self.tasks.__default_bash__} {cmdarg}')
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

        if not alias_set.empty and alias_set.get(action):
            action = alias_set.get(action)

        func = getattr(self.tasks, action, None)

        if func is None:
            return self.default_command()

        if not callable(func):
            return self.command_not_found(self.action)

        self.load_parameters(func)

        context = self.context_mapping.get(action)
        if isinstance(self.tasks.__options_handler__, type):
            args = self.tasks.__options_handler__().process_options(func, self.options, context)
        else:
            args = self.tasks.__options_handler__.process_options(func, self.options, context)

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
            output('    <shell> -h')
            output('    <shell> -h <action>')
            output('用法:')
            output('    <shell> <action> [options...]', end='\n\n')

            cm = sorted(self.tasks.__ls_task__)
            output('命令:')
            for k in cm:
                # func_name = self.tasks.__ls_task__[k]
                desc = desc_set.get(k)
                if not desc:
                    desc = find_description(getattr(self.tasks, k, None))

                alias = alias_set.find_alias(k)
                k = alias if alias else k

                if desc:
                    nspace = 18 - len(k)
                    if nspace > 0:
                        space = ' ' * nspace
                    else:
                        space = ''
                    desc = f'{space}{desc}'

                opt = f'    {k}{desc}'
                output(opt)
        sys.exit()


def run_cls(cls, dic, what=None, ex=None):
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

    ignore_set.add('__options_handler__')
    ignore_set.add('__default_bash__')
    ignore_set.add('__before__')
    ignore_set.add('__after__')
    ignore_set.add('cmd')

    def cmd(self, *args, **kwargs):
        return cmd(*args, **kwargs)

    def __before__(self):
        pass

    def __after__(self):
        pass


class Shell(Main, metaclass=GsMeta):
    pass
