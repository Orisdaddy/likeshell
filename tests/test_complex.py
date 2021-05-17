import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell import exceptions


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

    def task3(
            self,
            a1,
            a2: likeshell.Input,
            *,
            a3='default'
    ):
        assert a1 == 'arg1'
        assert isinstance(a2, likeshell.Input)
        assert a3 == 'default' or a3 == 'arg3'
        raise RuntimeError('run task3')

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
        raise RuntimeError('run task4')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestComplex(unittest.TestCase):
    def test_task1(self):
        # task1
        sys.argv = ['test.py', 'task1', 'arg1', 'arg2', 'arg3', 'arg4', 'arg5']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task1', str(e))

    def test_task2(self):
        # task2
        sys.argv = ['test.py', 'task2', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))

    def test_task3(self):
        # task3
        sys.argv = ['test.py', 'task3', 'arg1']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task3', str(e))

        sys.argv = ['test.py', 'task3', 'arg1', 'arg3']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task3', str(e))

    def test_task4(self):
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

    def test_task5(self):
        # task5
        sys.argv = ['test.py', 'task4', 'arg1', '--arg2', 'arg2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task4', str(e))
