# likeshell


## 要求

Python >= 3.6

## 安装

使用pip安装

```shell script
$ pip install like shell
```


## 简单使用

创建demo.py文件

```python
import likeshell

class MyTasks(likeshell.Shell):
    def test(self, s1: str, i1: int, f1: float):
        print(f's1 is {s1}')
        print(f'i1 is {i1}')
        print(f'f1 is {f1}')

```

```shell script
>> python demo.py test str1 100 10.01
<< s1 is str1
<< i1 is 100
<< f1 is 10.01
```