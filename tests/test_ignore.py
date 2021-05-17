import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import CommandError, COMMAND_NOT_FOUND


class MyTask(likeshell.Main):
    @likeshell.ignore
    def ignore_task(self):
        raise RuntimeError('run task1')

    def existence_task(self):
        raise RuntimeError('run task2')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestIgnore(unittest.TestCase):
    def test_ignore_task(self):
        sys.argv = ['test.py', 'ignore_task']
        try:
            run()
            assert False
        except CommandError as e:
            self.assertEqual(COMMAND_NOT_FOUND, e.code)
            self.assertEqual('Commend "ignore_task" is not found. Similar command: existence_task', e.message)

        sys.argv = ['test.py', 'existence_task']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))
