# 程序入口

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
