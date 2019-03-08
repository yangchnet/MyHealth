import threading
import time


class MyThread(threading.Thread):
    def __init__(self, arg):
        super(MyThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.arg = arg

    def run(self):
        time.sleep(1)
        print('the arg is:%s\r' % self.arg)


for i in range(4):
    t = MyThread(i)
    t.start()
