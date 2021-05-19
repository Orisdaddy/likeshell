# 可选参数

支持以`-a`、`--arg`绑定标签的形式定义参数


## 通过类型定义

```python
import likeshell

 
class MyTasks(likeshell.Shell):
    def task1(
            self,
            a1,
            a2: likeshell.Options(tag='--a2', arglen=2),
    ):
        """
        参数说明
            :tag: 可识别的标签名 多个使用元组或列表例如['-a', '--arg']
            :arglen: 指定接收的参数个数
        """
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
        """
        参数说明
            :arg: 可选参数对应的位置参数名称
            :tag: 可识别的标签名 多个使用元组或列表例如['-a', '--arg']
            :arglen: 指定接收的参数个数
        """
        print(a1, a2)
        assert a1 == 'hello'
        assert a2 == 'world'
```


```shell script
>> python demo.py task1 --a2 world -a1 hello
<< hello world
```
