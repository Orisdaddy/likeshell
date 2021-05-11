# 钩子

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
