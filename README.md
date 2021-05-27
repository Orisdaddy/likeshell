# likeshell

[![PyPI version](https://badge.fury.io/py/likeshell.svg)](https://badge.fury.io/py/likeshell)
[![Supported Versions](https://img.shields.io/pypi/pyversions/likeshell.svg)](https://pypi.org/project/likeshell)
[![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[![Actions Status](https://github.com/Orisdaddy/likeshell/workflows/Macos%20Test/badge.svg)](https://github.com/Orisdaddy/likeshell/actions)
[![codecov](https://codecov.io/gh/Orisdaddy/likeshell/branch/master/graph/badge.svg)](https://codecov.io/gh/Orisdaddy/likeshell)


likeshell 快速构建自己的命令行工具，扩展性强、可配置、开箱即用、干净整洁，只需一步构建自己的CLI。

likeshell通过定义类中方法的形式定义CLI中的命令，极少有任务逻辑外的代码，使用简单，使开发的CLI程序简洁易用可读性强。


## 要求

Python >= 3.6

## 安装

使用pip安装

```shell script
$ pip install likeshell
```


## 简单使用

1.创建一个python文件，这里命名为demo.py。

```python
import likeshell

class MyTasks(likeshell.Shell):  # 定义类并继承likeshell.Shell，类名并不影响程序。
    def task1(        # 命令名默认为方法名称
            self,     # 默认按顺序输入参数，self被忽略
            s1,       # 不指定类型则不校验
            i1: int,  # 指定类型会校验参数类型
            f1: float
        ):
        print('run test1')
        print(f's1 is {s1}')
        print(f'i1 is {i1}')
        print(f'f1 is {f1}')
    
    def task2(self):
        print('run test2')
```

2.在终端中输入。

```shell script
>> python demo.py task1 str1 100 10.01
<< run test1
   s1 is str1
   i1 is 100
   f1 is 10.01

>> python demo.py task1
<< likeshell.exceptions.ParameterError: MissingParameter: s1.

>> python demo.py task1 str1 str2 str3
<< likeshell.exceptions.ParameterError: ParameterTypeError: "str2" is not a int

>> python demo.py task2
<< run test2
```


## 功能文档
### 基础功能

- [基本使用](#基本使用)
- [参数](#参数)
- [钩子](#钩子)
- [帮助](#帮助)

### 高级功能

- [任务别名](#任务别名)
- [无视任务](#无视任务)
- [输入(input)](#输入)
- [可选参数](#可选参数)
- [命令执行](#命令执行)
- [程序入口](#程序入口)
- [配置](#配置)



## 基本使用

基础使用可完全使用Python语法，除继承操作外不需要使用`likeshell`中的任何方法。

1.创建命令类并继承`likeshell.Shell`
2.创建相应的命令任务(命令默认为方法名)
3.定义参数

```python
# 导入likeshell包
import likeshell

# 创建类并继承likeshell.Shell
class MyTasks(likeshell.Shell):
    # 创建相应的命令任务
    def task1(self, s1, i1, f1):
        print('run test1')
        print(f's1 is {s1}')
        print(f'i1 is {i1}')
        print(f'f1 is {f1}')
    
    def task2(self):
        print('run test2')
```

## 参数

任务中的参数定义

### 参数类型

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
<< likeshell.exceptions.ParameterError: ParameterTypeError: "str1" is not a int
```

### 可变长参数(*args)

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

### 非必要参数与默认值

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

## 钩子

```python
import likeshell

class GitShell(likeshell.Shell):
    # 在命令执行之前生效
    def __before__(self):
        print('run before')
    
    # 在命令执行之后生效
    def __after__(self):
        print('run after')
```

## 帮助

通过`-h`或`--help`获得方法相关的提示

```python
import likeshell

class MyTasks(likeshell.Shell):
    @likeshell.desc('This is task1')  # likeshell.desc定义命令的简要说明 在-h中打印 不定义默认打印comment多行注释中的有效内容第一行
    def task1(self, s1, i1, f1):
        """
        定义多行注释，help会将其作为命令说明打印
        task1说明:
            task1 takes 3 arguments
        """
        print('run test1')
        print(f's1 is {s1}')
        print(f'i1 is {i1}')
        print(f'f1 is {f1}')
    
    def task2(self):
        """
        task is a method
        """
        print('run test2')
```

```shell script
>> python demo.py
<< 帮助:
      <shell> -h
      <shell> -h <action>
   用法:
      <shell> <action> [options...]
    
   命令:
      task1             This is task1
      task2             task is a method


>> python demo.py -h task1
<< 定义多行注释，help会将其作为命令说明打印
   task1说明:
       task1 takes 3 arguments
```

## 任务别名

在程序中命令默认去匹配方法名，
当希望使用的命令名为python中关键字、包含特殊字符或希望定义的更加简短时，可以通过定义别名的方式实现。

likeshell提供两种方式来实现。

### 通过装饰器

使用`likeshell.alias`装饰器实现别名定义

```python
import likeshell

class MyTasks(likeshell.Shell):
    # 定义方法task1的别名为lambda
    @likeshell.alias('lambda')
    def task1(self):
        print('run task1')
```

```shell script
>> python demo.py lambda
<< run task1
```

### 通过多行注释
在方法中定义`:alias`开头的多行注释 
通过空格` `或`:`分割实现别名定义

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(self):
        """
        定义方法task1的别名为lambda
        
        :alias: lambda
        """
        print('run task1')
```

```shell script
>> python demo.py lambda
<< run task1
```

## 无视任务

让指定任务命令不再被识别，也无法再调用

### 通过装饰器

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

## 输入

实现用户输入

### 使用

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

### 参数说明

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
            :default: 输入为空时 使用默认值 也可以通过定义参数默认值实现
            :hide: 隐藏输入内容 默认为False
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

## 可选参数

支持以`-a`、`--arg`绑定标签的形式定义参数


### 通过类型定义

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


### 通过装饰器

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
            :tag: 可识别的标签名 要定义多个标签则使用元组或列表 例如['-a', '--arg']
            :arglen: 指定接收的参数个数 
                     定义为0 将会接收到为'exist'的字符串或默认值
                     默认定义为1 接收指定的字符串或默认值
                     定义为大于1的数组 接收多个参数的列表或默认值
        """
        print(a1, a2)
        assert a1 == 'hello'
        assert a2 == 'world'
```


```shell script
>> python demo.py task1 --a2 world -a1 hello
<< hello world
```

## 命令执行

### 使用

```python
import likeshell


class MyTasks(likeshell.Shell):
    def task1(self):
        self.cmd('git branch')
        # likeshell.cmd('git branch')  # 两者效果一样

        # p = self.cmd('git branch', popen=True)  # 通过子进程执行命令
        # print(p.pid)
```

```shell script
>> python demo.py task1
>> * master
```

## 程序入口

当CLI程序需要配置入口时

```python
import likeshell
from likeshell.shell import run_cls

 
class MyTasks(likeshell.Main):  # 继承 likeshell.Main
    def task1(self):
        print('run task1')


def run():
    # 调用run_cls方法
    run_cls(MyTasks, MyTasks.__dict__)

```

## 配置

```python
import likeshell

class MyTasks(likeshell.Shell):
    __default_bash__ = 'git'  # 命令未击中时 可以使用其他cli (默认为None)
    __options_handler__ = likeshell.SimpleOptionsHandler()  # 参数处理器

    def task1(self):
        print('run task1')
```
