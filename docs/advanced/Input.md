# 输入

## 使用

```python
import likeshell


class MyTasks(likeshell.Shell):
    def task1(
            self,
            a: likeshell.Input  # 定义类型为 likeshell.Input
        ):
        print('run task1')
        res = a.input()  # .input()方法开始输入
        print(res)
```

```shell script
>> python demo.py task1
>> a:
>> a: hello world
<< run task1
   hello world
```

## 参数说明

```python
import likeshell


class MyTasks(likeshell.Shell):
    def task1(
            self,
            a: str,
            b: likeshell.Input,
            c: str
    ):
        def valid(arg):
            arg += '!'
            return arg

        print('run task1')
        res = b.input(
            message='username:',  # message: 输入提示信息
            callback=valid,  # callback: 接收一个回调函数 接收一个参数，返回一个参数
            hide=True  # hide: 隐藏输入的内容
        )
        print(a)
        print(res)
        print(c)
```

```shell script
>> python demo.py task1 astr cstr
<< run task1
>> username: joker
<< astr
   joker!
   cstr
```