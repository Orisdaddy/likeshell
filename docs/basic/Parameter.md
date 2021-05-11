# 参数

任务中的参数定义

## 参数类型

通过type annotation语法增加类型校验

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(self, s1):
        print(f's1 is {s1}')
    
    def task2(self, i1: int):
        print(f'i1 is {i1}')
```

```shell script
>> python demo.py task1 100
<< s1 is 100

>> python demo.py task2 str1
<< TypeError: "str1" is not a int
```

## 可变长参数(*args)

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(self, *args):
        print(f'args: {args}')
```

```shell script
>> python demo.py task1 a1 a2 a3
<< args: ['a1', 'a2', 'a3']
```

## 非必要参数与默认值

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(
            self,
            s1: str,
            *,  # 通过*分割必要参数与非必要参数
            s2: str = 'string'
        ):
        print(f's1: {s1}')
        print(f's2: {s2}')
```

```shell script
>> python demo.py task1 str1
<< s1: str1
   s2: string

>> python demo.py task1 str1 str2
<< s1: str1
   s2: str2
```
