import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import DefinitionError


class MyTask(likeshell.Main):
    @likeshell.Options(arg='a1', tag='-a')
    def options(self, a1):
        assert a1 == 'arg1'
        raise RuntimeError('run task1')

    @likeshell.Options(arg='a1', tag='-a', arglen=2)
    def mul_options(self, a1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task2')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestOptions(unittest.TestCase):
    def test_options(self):
        sys.argv = ['test.py', 'options', '-a', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task1', str(e))

    def test_mul_options(self):
        sys.argv = ['test.py', 'mul_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))

        sys.argv = ['test.py', 'mul_options', '-a', 'arg1']
        try:
            run()
            assert False
        except DefinitionError as e:
            self.assertEqual('"a1"[-a] missing 1 required parameters', str(e))

        sys.argv = ['test.py', 'mul_options', '-a', 'arg1', 'arg2', 'arg3']
        try:
            run()
            assert False
        except DefinitionError as e:
            self.assertEqual('"a1" takes 2 parameters but 3 were given', str(e))
