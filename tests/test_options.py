import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import DefinitionError, ParameterError


class MyTask(likeshell.Main):
    @likeshell.Options(arg='a1', tag='-a')
    def options(self, a1):
        assert a1 == 'arg1'
        raise RuntimeError('run task1')

    @likeshell.Options(arg='a1', tag='-a', arglen=2)
    def arg_mul_options(self, a1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task2')

    @likeshell.Options(arg='a1', tag=('-a', '--arg1'), arglen=2)
    def mul_tag_options(self, a1):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task3')

    def type_options(self, a1: likeshell.Options(tag='-a', arglen=2)):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task4')

    def type_mul_tag_options(self, a1: likeshell.Options(tag=['-a', '--arg1'], arglen=2)):
        assert a1 == ['arg1', 'arg2']
        raise RuntimeError('run task5')

    @likeshell.Options(arg='a1', tag='-a1')
    @likeshell.Options(arg='a2', tag='-a2')
    def mul_options(self, a1, a2):
        assert a1 == 'arg1'
        assert a2 == 'arg2'
        raise RuntimeError('run task6')

    @likeshell.Options(arg='a1', tag='-a1')
    @likeshell.Options(arg='a2', tag='-a2', arglen=0)
    def mark_options(self, a1, a2):
        assert a1 == 'arg1'
        assert a2 == 'exist'
        raise RuntimeError('run task7')


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
        sys.argv = ['test.py', 'arg_mul_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))

        sys.argv = ['test.py', 'arg_mul_options', '-a', 'arg1']
        try:
            run()
            assert False
        except ParameterError as e:
            self.assertEqual('MissingParameter: "a1"[-a] missing 1 required parameters.', str(e))

        sys.argv = ['test.py', 'arg_mul_options', '-a', 'arg1', 'arg2', 'arg3']
        try:
            run()
            assert False
        except ParameterError as e:
            self.assertEqual('MissingParameter: "a1" takes 2 parameters but 3 were given.', str(e))

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

    def test4_type_options(self):
        sys.argv = ['test.py', 'type_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task4', str(e))

    def test5_type_mul_tag_options(self):
        sys.argv = ['test.py', 'type_mul_tag_options', '-a', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task5', str(e))

        sys.argv = ['test.py', 'type_mul_tag_options', '--arg1', 'arg1', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task5', str(e))

    def test6_mul_options(self):
        sys.argv = ['test.py', 'mul_options', '-a2', 'arg2', '-a1', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task6', str(e))

    def test7_mark_options(self):
        sys.argv = ['test.py', 'mark_options', '-a2', '-a1', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task7', str(e))

        sys.argv = ['test.py', 'mark_options', '-a1', 'arg1', '-a2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task7', str(e))

        sys.argv = ['test.py', 'mark_options', '-a1', 'arg1']
        try:
            run()
            assert False
        except ParameterError as e:
            self.assertEqual('MissingParameter: a2.', str(e))

    def test999_definition_error(self):
        from likeshell.context import empty_set

        empty_set()

        # duplicate tag
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                @likeshell.Options(arg='b', tag='--arg')
                def task1(self, a, b):
                    pass
            assert False
        except DefinitionError as e:
            self.assertEqual('Duplicate tag: --arg', str(e))
        empty_set()

        # define default value
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                @likeshell.Options(arg='b', tag='-b')
                def task1(self, a, *, b):
                    pass
            assert False
        except DefinitionError as e:
            self.assertEqual('Parameters after `*` need to define default value', str(e))
        empty_set()

        # positional parameter and parameter decorated by `Options`
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(arg='a', tag=['--arg', '-a'])
                def task1(self, a, b):
                    pass
            assert False
        except DefinitionError as e:
            self.assertEqual('Cannot define positional parameter after parameter decorated by `Options`.', str(e))
