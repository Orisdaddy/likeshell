# 可选参数

支持以`-a`、`--arg`绑定标签的形式定义参数


## 通过定义model

```python
import likeshell


class Arg2(likeshell.Options):
    tag = '--a2'
    arglen = 2  # 指定接收几个参数


class MyTasks(likeshell.Shell):
    def task1(
            self,
            a1,
            a2: Arg2,
    ):
        print(a1, a2[0], a2[1])
        assert a1 == 'hello'
        assert a2 == ['world', '!']
```

```shell script
>> python demo.py task1 hello --a2 world !
<< hello world !
```


## 通过装饰器

```python
import likeshell


class MyTasks(likeshell.Shell):
    @likeshell.Options(arg='a1', tag='--a1')
    @likeshell.Options(arg='a2', tag='--a2')
    def task1(
            self,
            a1,
            a2,
    ):
        print(a1, a2)
        assert a1 == 'hello'
        assert a2 == 'world'
```


```shell script
>> python demo.py task1 --a2 world -a1 hello
<< hello world
```
