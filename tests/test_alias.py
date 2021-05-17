import sys
import likeshell
import unittest

from likeshell.shell import run_cls


class MyTask(likeshell.Main):
    @likeshell.alias('runalias')
    def alias1(self):
        raise RuntimeError('run task1')

    def alias2(self):
        """
        run alias2
        :alias a2
        """
        raise RuntimeError('run task2')


def run():
    run_cls(MyTask, MyTask.__dict__)


class TestAlias(unittest.TestCase):
    def test_alias1(self):
        sys.argv = ['test.py', 'runalias']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task1', str(e))

    def test_alias2(self):
        sys.argv = ['test.py', 'a2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))
