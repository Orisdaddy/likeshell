# 帮助

通过`-h`获得方法相关的提示

```python
import likeshell

class MyTasks(likeshell.Shell):
    def task1(self, s1, i1, f1):
        """
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
      task1
      task2

>> python demo.py -h task1
<< task1说明:
       task1 takes 3 arguments
```