import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import DefinitionError


class MyTask(likeshell.Main):
    def task1(
            self,
            a1,
            a2='default',
            *args
    ):
        assert a1 == 'arg1'
        assert a2 == 'arg2'
        assert args == ('arg3', 'arg4', 'arg5')
        raise RuntimeError('run task1')

    def task2(
            self,
            a1,
            a2='default',
            *args
    ):
        assert a1 == 'arg1'
        assert a2 == 'default'
        assert args == tuple()
        raise RuntimeError('run task2')

    @likeshell.Options(tag='--arg2', arg='a2')
    def task4(
            self,
            a1,
            *,
            a2='default val',
    ):
        assert a1 == 'arg1'
        assert a2 == 'arg2' or a2 == 'default val'
        raise RuntimeError('run task4')

    @likeshell.Options(tag='--arg2', arg='a2')
    @likeshell.Options(tag='--arg3', arg='a3')
    def task5(
            self,
            a1,
            a2,
            *,
            a3='default val'
    ):
        assert a1 == 'arg1'
        assert a2 == 'arg2'
        assert a3 == 'default val'
        raise RuntimeError('run task5')

    @likeshell.Options(tag='--arg2', arg='a2')
    @likeshell.Options(tag='--arg3', arg='a3')
    @likeshell.Options(tag='--arg4', arg='a4', arglen=2)
    @likeshell.Options(tag='--arg5', arg='a5', arglen=2)
    def task6(
            self,
            a1,
            a2: int,
            a3: float,
            a4: int,
            *,
            a5: float = [10.1, 20.2]
    ):
        assert a1 == 'arg1'
        assert a2 == 10
        assert a3 == 10.1
        assert a4 == [10, 20]
        assert a5 == [10.1, 20.2]
        raise RuntimeError('run task6')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestComplex(unittest.TestCase):
    def test1_task1(self):
        # task1
        sys.argv = ['test.py', 'task1', 'arg1', 'arg2', 'arg3', 'arg4', 'arg5']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task1', str(e))

    def test2_task2(self):
        # task2
        sys.argv = ['test.py', 'task2', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))

    def test4_task4(self):
        # task4
        sys.argv = ['test.py', 'task4', 'arg1', '--arg2', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task4', str(e))

        sys.argv = ['test.py', 'task4', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task4', str(e))

    def test5_task5(self):
        # task5
        sys.argv = ['test.py', 'task5', 'arg1', '--arg2', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task5', str(e))

    def test6_task6(self):
        # task5
        sys.argv = ['test.py', 'task6', 'arg1', '--arg2', '10', '--arg3', '10.1', '--arg4', '10', '20']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task6', str(e))

    def test7_definition_error(self):
        from likeshell.context import empty_set

        empty_set()
        # Options and Input
        try:
            class Task(likeshell.Shell):
                @likeshell.Options(tag='--arg', arg='a1')
                def task7(
                        self,
                        a1: likeshell.Input,
                ):
                    raise RuntimeError('run task7')
            assert False
        except DefinitionError as e:
            self.assertEqual('Parameter decorated by `Options` cannot be defined as `Input` parameter', str(e))

        empty_set()
