# 命令执行

## 使用

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
