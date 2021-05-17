# likeshell

[![PyPI version](https://badge.fury.io/py/likeshell.svg)](https://badge.fury.io/py/likeshell)
[![Actions Status](https://github.com/Orisdaddy/likeshell/workflows/Python%20Test/badge.svg)](https://github.com/Orisdaddy/likeshell/actions)
[![codecov](https://codecov.io/gh/Orisdaddy/likeshell/branch/master/graph/badge.svg)](https://codecov.io/gh/Orisdaddy/likeshell)


likeshell 快速构建自己的命令行工具，扩展性强、可配置、开箱即用、干净整洁，
只需一步构建自己的CLI。

## 要求

Python >= 3.6

## 安装

使用pip安装

```shell script
$ pip install likeshell
```


## 简单使用

创建demo.py文件

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(
            self,
            s1: str, # 不指定类型则不校验
            i1: int,
            f1: float
        ):
        print('run test1')
        print(f's1 is {s1}')
        print(f'i1 is {i1}')
        print(f'f1 is {f1}')
    
    def task2(self):
        print('run test2')

```

```shell script
>> python demo.py task1 str1 100 10.01
<< run test1
   s1 is str1
   i1 is 100
   f1 is 10.01

>> python demo.py task1
<< ValueError: Miss parameter "s1"

>> python demo.py task1 str1 str2 str3
<< TypeError: "str2" is not a int

>> python demo.py task2
<< run test2

```


## 功能文档
### 基础功能

- [基本使用](docs/basic/Usage.md)
- [参数](docs/basic/Parameter.md)
- [钩子](docs/basic/Hook.md)
- [配置](docs/basic/Config.md)
- [帮助](docs/basic/Help.md)

### 高级功能

- [任务别名](docs/advanced/Alias.md)
- [无视任务](docs/advanced/Ignore.md)
- [程序入口](docs/advanced/Main.md)
- [输入(input)](docs/advanced/Input.md)
- [可选参数](docs/advanced/Options.md)
