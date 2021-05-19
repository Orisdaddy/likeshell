import sys
import likeshell
import unittest
import subprocess
import os

from likeshell.shell import run_cls

rootpath = os.path.dirname(os.path.dirname(__file__))
os.environ['PYTHONPATH'] = rootpath


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

    def test_input_task(self):
        test_path = os.path.join(rootpath, "tests", "input_task.py")
        p = subprocess.Popen(
            f'python {test_path} input',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        out, err = p.communicate('arg1\n')
        self.assertEqual('', err)

        p = subprocess.Popen(
            f'python {test_path} input_pwd',
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        out, err = p.communicate('\n')
        self.assertEqual('', err)
