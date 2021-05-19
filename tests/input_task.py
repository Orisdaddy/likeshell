import likeshell


class MyTask(likeshell.Shell):
    def input(self, a: likeshell.Input):
        user = a.input()
        assert user == 'arg1'

    def input_pwd(self, a: likeshell.Input):
        pwd = a.input(message='password:', default='pwd')
        assert pwd == 'pwd'
