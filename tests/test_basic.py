import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell import exceptions


class MyTask(likeshell.Main):
    def task(self):
        """
        task comment
        """
        raise RuntimeError('run task')

    def params(
            self,
            arg1,
            arg2,
            arg3,
    ):
        if arg1 != 'hello':
            raise ValueError(f'arg1 != hello')
        if arg2 != 'world':
            raise ValueError(f'arg2 != world')
        if arg3 != '!':
            raise ValueError(f'arg3 != !')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestBasic(unittest.TestCase):
    def test_task(self):
        sys.argv = ['test.py', 'task']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task', str(e))

        sys.argv = ['test.py']
        try:
            run()
            assert False
        except SystemExit:
            pass

        sys.argv = ['test.py', '-h', 'task']
        try:
            run()
            assert False
        except SystemExit:
            pass

    def test_param(self):
        sys.argv = ['test.py', 'params', 'hello', 'world', '!']
        run()

        sys.argv = ['test.py', 'params', 'hello', 'world', '?']
        try:
            run()
            assert False
        except ValueError as e:
            self.assertEqual('arg3 != !', str(e))

        sys.argv = ['test.py', 'params', 'hello']
        try:
            run()
            assert False
        except exceptions.ParameterError as e:
            self.assertEqual('MissingParameter: arg2.', str(e))

        sys.argv = ['test.py', 'params', 'hello', 'world']
        try:
            run()
            assert False
        except exceptions.ParameterError as e:
            self.assertEqual('MissingParameter: arg3.', str(e))


