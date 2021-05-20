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


def adapt_linesep(content):
    if '\r\n' in content:
        nl = '\r\n'
    elif '\n' in content:
        nl = '\n'
    elif '\r' in content:
        nl = '\r'
    else:
        nl = os.linesep
    return nl
