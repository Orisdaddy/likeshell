# 配置

```python
import likeshell

class MyTasks(likeshell.Shell):
    __default_bash__ = 'git'  # 命令未击中时 可以使用其他cli (默认为None)
    __options_handler__ = likeshell.SimpleOptionsHandler()  # 参数处理器

    def task1(self):
        print('run task1')
```
