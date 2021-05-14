import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell import exceptions


class MyTask(likeshell.Main):
    def __before__(self):
        pass

    def __after__(self):
        pass

    def task(self):
        raise RuntimeError('run task')


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
