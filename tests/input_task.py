import likeshell


class MyTask(likeshell.Shell):
    def input(self, a: likeshell.Input):
        assert a == 'arg1'

    def input_pwd(
            self,
            a1,
            *,
            a2: likeshell.Input(prompt='password') = 'pwd'
    ):
        assert a1 == 'arg1'
        assert a2 == 'pwd'
