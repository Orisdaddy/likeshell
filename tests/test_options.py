import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import DefinitionError, ParameterError


class Arg1(likeshell.Options):
    arglen = 2
    tag = '-a'


class MulTagArg1(likeshell.Options):
    arglen = 2
    tag = ('-a', '--arg1')


class MyTask(likeshell.Main):
    @likeshell.Options(arg='a1', tag='-a')
    def options(self, a1):
        assert a1 == 'arg1'
        raise RuntimeError('run task1')

    @likeshell.Options(arg='a1', tag='-a', arglen=2)
    def mul_options(self, a1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task2')

    @likeshell.Options(arg='a1', tag=('-a', '--arg1'), arglen=2)
    def mul_tag_options(self, a1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task3')

    def model_options(self, a1: Arg1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task4')

    def model_mul_tag_options(self, a1: MulTagArg1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task5')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestOptions(unittest.TestCase):
    def test1_options(self):
        sys.argv = ['test.py', 'options', '-a', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task1', str(e))

        sys.argv = ['test.py', 'options']
        try:
            run()
            assert False
        except ParameterError as e:
            self.assertEqual('MissingParameter: a1.', str(e))

    def test2_mul_options(self):
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

    def test3_mul_tag_options(self):
        sys.argv = ['test.py', 'mul_tag_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task3', str(e))

        sys.argv = ['test.py', 'mul_tag_options', '--arg1', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task3', str(e))

    def test4_model_options(self):
        sys.argv = ['test.py', 'model_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task4', str(e))

    def test5_model_mul_tag_options(self):
        sys.argv = ['test.py', 'model_mul_tag_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task5', str(e))

        sys.argv = ['test.py', 'model_mul_tag_options', '--arg1', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task5', str(e))

    def test6_definition_error(self):
        from likeshell.context import empty_set

        empty_set()

        # duplicate tag
        sys.argv = ['test.py', 'task1']
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                @likeshell.Options(arg='b', tag='--arg')
                def task1(self, a, b):
                    pass
        except DefinitionError as e:
            self.assertEqual('Duplicate tag: --arg', str(e))
        empty_set()

        # define default value
        sys.argv = ['test.py', 'task1']
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                @likeshell.Options(arg='b', tag='-b')
                def task1(self, a, *, b):
                    pass
        except DefinitionError as e:
            self.assertEqual('Parameters after `*` need to define default value', str(e))
        empty_set()

        # positional parameter and parameter decorated by `Options`
        sys.argv = ['test.py', 'task1']
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                def task1(self, a, b):
                    pass
        except DefinitionError as e:
            self.assertEqual('Cannot define positional parameter after parameter decorated by `Options`.', str(e))
