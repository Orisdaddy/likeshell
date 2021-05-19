import os
import subprocess


def cmd(arg,
        popen=False,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        ):
    if popen:
        return subprocess.Popen(arg,
                                shell=True, stdin=stdin,
                                stdout=stdout, stderr=stderr,
                                universal_newlines=True)
    else:
        os.system(arg)
