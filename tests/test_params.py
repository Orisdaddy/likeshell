import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell import exceptions


class MyTask(likeshell.Main):
    def params_args(self, *args):
        if len(args) != 3:
            raise ValueError('len(args) != 3')

    def params_type(
            self,
            arg1,
            arg2: int,
            arg3: float,
            arg4: int,
    ):
        if arg1 != 'a1':
            raise ValueError(f'arg1 != a1')
        if arg2 != 100:
            raise ValueError(f'arg2 != 100')
        if arg3 != 100.1:
            raise ValueError(f'arg3 != 100.1')
        if arg4 != -100:
            raise ValueError(f'arg4 != -100')

    def params_default(
            self,
            arg1,
            *,
            arg2='default val'
    ):
        if arg2 != 'default val':
            raise ValueError('arg2 != default val')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestParamsType(unittest.TestCase):
    def test_params_args(self):
        command = 'params_args'

        sys.argv = ['test.py', command, 'a1', 'a2', 'a3']
        run()

        sys.argv = ['test.py', command, 'a1', 'a2']
        try:
            run()
            assert False
        except ValueError as e:
            self.assertEqual('len(args) != 3', str(e))

    def test_params_default(self):
        command = 'params_default'

        sys.argv = ['test.py', command, 'a1']
        run()

        sys.argv = ['test.py', command, 'a1', 'default']
        try:
            run()
            assert False
        except ValueError as e:
            self.assertEqual('arg2 != default val', str(e))

    def test_params_type(self):
        command = 'params_type'

        sys.argv = ['test.py', command, 'a1', '100', '100.1', '-100']
        run()

        sys.argv = ['test.py', command, 'hello', '100', '100.1', '-100']
        try:
            run()
            assert False
        except ValueError as e:
            self.assertEqual('arg1 != a1', str(e))

        sys.argv = ['test.py', command, 'a1', '100.1', '100.1', '-100']
        try:
            run()
            assert False
        except exceptions.ParameterError as e:
            self.assertEqual('ParameterTypeError: "100.1" is not a int', str(e))

        sys.argv = ['test.py', command, 'a1', '100', 'str', '-100']
        try:
            run()
            assert False
        except exceptions.ParameterError as e:
            self.assertEqual('ParameterTypeError: "str" is not a float', str(e))

        sys.argv = ['test.py', command, 'a1', '100', '100.1', '-100.1']
        try:
            run()
            assert False
        except exceptions.ParameterError as e:
            self.assertEqual('ParameterTypeError: "-100.1" is not a int', str(e))
