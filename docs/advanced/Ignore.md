# 无视任务

## 通过装饰器

使用`likeshell.ignore`装饰器无视指定的方法

```python
import likeshell

class MyTasks(likeshell.Shell):
    @likeshell.ignore
    def task1(self):
        print('run task1')
```

```shell script
>> python demo.py task1
<< RuntimeError: task1 is not found.
```