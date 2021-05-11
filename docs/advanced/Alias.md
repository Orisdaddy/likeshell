# 任务别名

出现命令名为python中关键字或希望定义的更加简短时，可以通过定义别名的方式实现。

## 通过多行注释
定义`:alias`开头的注释 通过空格` `或`:`分割实现别名定义

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(self):
        """
        :alias: lambda
        :alias lambda
        """
        print('run task1')
```

```shell script
>> python demo.py lambda
<< run task1
```


## 通过装饰器

使用`likeshell.alias`装饰器实现别名定义

```python
import likeshell

class MyTasks(likeshell.Shell):
    @likeshell.alias('lambda')
    def task1(self):
        print('run task1')
```

```shell script
>> python demo.py lambda
<< run task1
```
