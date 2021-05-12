# 基本使用

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