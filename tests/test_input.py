import sys
import likeshell
import unittest

from likeshell.shell import run_cls


class MyTask(likeshell.Main):
    def input(self, a1: likeshell.Input):
        assert isinstance(a1, likeshell.Input)
        raise RuntimeError('run task')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestBasic(unittest.TestCase):
    def test_input(self):
        sys.argv = ['test.py', 'input']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task', str(e))
