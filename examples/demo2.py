import os
import sys
import time
import likeshell
import subprocess

sys.argv = ['test.py', 'delete_branch', 'dev']

pop = subprocess.Popen

upstream = 'upstream'
default_branch = 'master'

std = {
    'shell': True,
    'stdout': sys.stdout,
    'stdin': sys.stdin,
    'stderr': sys.stderr
}

user_config = {
    'github': {
        'name': 'github name',
        'email': 'xxxx@xx.com'
    },
    'gitlab': {
        'name': 'gitlab name',
        'email': 'xxxx@xx.com'
    },
}


class GitShell(likeshell.Shell):
    def __before__(self):
        self.pop_list = []

    def __after__(self):
        for p in self.pop_list:
            p.wait()

    def get_current_branch(self) -> str:
        p = pop('git branch --show-current', shell=True, stdout=subprocess.PIPE)
        b = p.stdout.read()
        return b.decode('utf-8').strip('\n')

    def fork_reset(
            self,
            version: str
    ):
        os.system(f'git checkout {default_branch}')
        os.system(f'git reset --hard {version}')
        os.system(f'git push -f -u origin {default_branch}')

    def fork(
            self,
            address: str,
            upstream_address: str,
            *,
            alias: str = ''
    ):
        """
        Fork repo

        gitshell fork <repo> <remote repo> [alias]

        :param address: fork repository https/ssh address
        :param upstream_address:
        :param alias: dir alias
        """
        if alias:
            dir_name = alias
        else:
            dir_name = address.split('/').pop()[:-4]
        os.system(
            f'git clone {address} {alias} && cd {dir_name} && git remote add {upstream} {upstream_address}')

    def update_fork(self):
        """
        Update fork repo

        gitshell update_fork
        """
        os.system(f'git checkout {default_branch}')
        cmd = f'git fetch {upstream} && git rebase {upstream}/master && git push origin'
        os.system(cmd)

    def update_fork_checkout(
            self,
            branch_name: str,
            *,
            is_write: int = '1'
    ):
        """
        update fork repo & create a new branch
        """
        os.system(f'git checkout {default_branch}')

        if is_write == '1':
            is_write = True
        else:
            is_write = False

        if is_write:
            cmd = f'git pull && git checkout -b {branch_name}'
        else:
            cmd = f'git fetch {upstream} && git rebase {upstream}/master &&' \
                  f' git push origin && git checkout -b {branch_name}'
        os.system(cmd)

    def update_branch(
            self,
            branch_name: str,
            *,
            is_write: int = 1
    ):
        """
        Update branch
        """
        os.system(f'git checkout {default_branch}')

        if is_write == 1:
            is_write = True
        else:
            is_write = False

        if is_write:
            cmd = f'git pull &&git checkout {branch_name} &&' \
                  f' git rebase master && git push -u origin {branch_name} --force'
        else:
            cmd = f'git fetch {upstream} && git rebase {upstream}/master && git push origin &&' \
                  f' git checkout {branch_name} && git rebase master && git push -u origin {branch_name} --force'
        os.system(cmd)

    def set_user_config(
            self,
            user: str,
            *,
            email: str = ''
    ):
        """
        Set username & email

        1. gitshell set_user_config <config key>
        2. gitshell set_user_config <username> <email>
        """
        if user in user_config:
            username = user_config[user]['name']
            email = user_config[user]['email']
        else:
            username = user

        os.system(f'git config --global user.name "{username}"')
        os.system(f'git config --global user.email "{email}"')

    def delete_branch(self, *args):
        """
        Delete branch

        gitshell delete_branch <branch1> <branch2> ...
        """
        os.system(f'git checkout {default_branch}')

        # delete branch
        time.sleep(0.5)
        for name in args:
            cmd1 = f'git branch -D {name}'
            cmd2 = f'git push origin --delete {name}'

            pop(cmd1, **std)
            p = pop(cmd2, **std)
            self.pop_list.append(p)

    def amend_config(
            self,
            user: str,
            *,
            email: str = ''
    ):
        """
        Amend username & email

        1. gitshell amend_config <config key>
        2. gitshell amend_config <username> <email>
        """
        if user in user_config:
            username = user_config[user]['name']
            email = user_config[user]['email']
        else:
            username = user
        if self.get_current_branch() == default_branch:
            raise PermissionError(f'push {default_branch}')

        os.system(f'git commit --amend --author "{username} <{email}>"')
        os.system(f'git push --force-with-lease origin {self.get_current_branch()}')

    def amend_push(self):
        """
        Amend & force push

        gitshell amend_push
        """
        if self.get_current_branch() == default_branch:
            raise PermissionError(f'push {default_branch}')

        os.system('git commit --amend')
        os.system(f'git push --force-with-lease origin {self.get_current_branch()}')
