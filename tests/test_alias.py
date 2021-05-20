import sys
import likeshell
import unittest

from likeshell.shell import run_cls
from likeshell.exceptions import DefinitionError


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

    def alias3(self):
        """
        run alias3
        :alias: a3
        """
        raise RuntimeError('run task3')


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

        sys.argv = ['test.py', '-h', 'runalias']
        try:
            run()
            assert False
        except SystemExit:
            pass

    def test_alias2(self):
        sys.argv = ['test.py', 'a2']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task2', str(e))

    def test_alias3(self):
        sys.argv = ['test.py', 'a3']
        try:
            run()
            assert False
        except RuntimeError as e:
            self.assertEqual('run task3', str(e))

    def test_tag_missing(self):
        try:
            class TestTask(likeshell.Shell):
                @likeshell.alias('alias')
                def alias1(self):
                    pass

                @likeshell.alias('alias')
                def alias2(self):
                    pass
            assert False
        except DefinitionError as e:
            self.assertEqual('The aliases of "alias1" and "alias2" are duplicated', str(e))