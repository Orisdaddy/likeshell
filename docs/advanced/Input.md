# 输入

实现用户输入

## 使用

```python
import likeshell


class MyTasks(likeshell.Shell):
    def task1(
            self,
            a: likeshell.Input  # 定义类型为 likeshell.Input
        ):
        print('run task1')
        print(a)
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


def valid(arg):
    arg += '!'
    return arg


class MyTasks(likeshell.Shell):
    def task1(
            self,
            a: str,
            b: likeshell.Input(prompt='username:', default='default', hide=False, callback=valid),
            c: str
    ):
        """
        参数说明
            :prompt: 输入时显示的提示字符串
            :default: 输入为空时 使用默认值
            :hide: 隐藏输入内容
            :callback: 回调函数 要求接收一个参数 返回一个参数
        """
        print('run task1')
        print(a)
        print(b)
        print(c)
```

```shell script
>> python demo.py task1 astr cstr
>> username: joker
<< run task1
   astr
   joker!
   cstr
```