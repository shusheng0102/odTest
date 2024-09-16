## day16.并发编程2

## 1.线程理论

```
'''
1 什么是线程
    进程其实一个资源单位（开启一个内存空间，里面放应该执行的代码，代码运行产生的数据）,
    而进程内的线程才是cpu上的执行单位
    进程是资源单位 qq资源 相当于一个车间 造发动机和造轮胎能共享吗
    线程其实指的就是代码的执行过程（开空间没关系，数据往进程去要）
    线程就是车间流水线  跟车间要
    至少有一个线程  一个车间也可以有多少流水线
2 为何要用线程
    线程vs进程
         1. 同一进程下的多个线程共享该进程内的资源
        2. 创建线程的开销要远远小于进程
    并发2种
         多进程实际上是每个进程里面单独一个线程
            由于进程当中资源不共享
            并发多个任务需要通信需要利用管道或者队列
         多线程是指同一个进程里面多个线程
            本身同一个进程里面多个线程资源就共享
            所以不需要借助任何的机制，数据之间就可以交互
3 如何用线程
'''
```

## 2.开启线程的方式

```
from threading import Thread
import  time
def task(name):
    print('%s is runing'%name)
    time.sleep(2)
    print('%s is done'%name)
if __name__ == '__main__':
    t = Thread(target=task,args=('线程1',))
    # 造线程非常快，因为不用开辟空间了
    t.start()
    print('主')

```

## 3.线程特性介绍

```
from threading import Thread,active_count,current_thread
import time,os
n = 100
def task():
    global n
    print('%s is running'%os.getpid())
    print('子%s'%current_thread().name)
    n = 0
    time.sleep(3)

if __name__ == '__main__':
    t = Thread(target=task)
    # 开启子线程
    t.start()
    # 等待子线程运行完
    t.join()
    # 线程的个数
    print(active_count())
    # 线程所在的进程pid
    print('主%s'%os.getpid())
    # 线程的名字
    print('主%s'%current_thread().name)
    # 同一个进程的所有线程资源共享
    print(n)


```

## 4.守护线程

```
from threading import Thread,active_count,current_thread
import time,os
n = 100
def task():
    global n
    print('%s is running'%os.getpid())
    print('子%s'%current_thread().name)
    n = 0
    time.sleep(3)

if __name__ == '__main__':
    t = Thread(target=task)
    # 开启子线程
    t.start()
    # 等待子线程运行完
    t.join()
    # 线程的个数
    print(active_count())
    # 线程所在的进程pid
    print('主%s'%os.getpid())
    # 线程的名字
    print('主%s'%current_thread().name)
    # 同一个进程的所有线程资源共享
    print(n)


```

## 5.线程互斥锁

```
from threading import Thread,Lock
import time
n = 100
mutex=Lock()
def task():
    global n
    # 线程1加锁
    mutex.acquire()
    temp = n
    # 在这个时间消耗完之前，后面的99个线程都进来了
    # 并且拿到的是temp=100
    # 效率高了，不安全
    # IO操作切换线程
    time.sleep(0.1)

    n = temp -1
    # 线程1计算完成释放锁
    mutex.release()
if __name__ == '__main__':
    t_l = []
    start = time.time()
    for i in range(100):
        t = Thread(target=task)
        t_l.append(t)
        t.start()
    for t in t_l:
        t.join()
    print(n,time.time()-start)





```

## 6.GIL全局解释器锁

```
'''
1. 什么是GIL(全局解释器锁)
    互斥锁就是把多个任务的共享数据的修改由并发变成串行
    代码运行先拿到cpu的权限，还需要把代码丢给解释器，再在进程里面的线程运行

    GIL本质就是一把互斥锁,相当于执行权限
    每个进程内都会存在一把GIL,同一进程内的多个线程
    必须抢到GIL之后才能使用解释器来执行自己的代码,
    即同一进程下的多个线程无法实现并行,
    用不了多核（多个cpu）优势
    但是可以实现并发
    因为多线程是遇到io操作就会释放GIL锁
2. 为何要有GIL
    垃圾回收机制不是线程安全的
    每个进程内都会存在一把GIL
        意味着有锁才能计算
        多进程适合处理计算密集型
    多线程适合处理io密集型 所以多线程多核优势没有意义
3. 如何用GIL
    有了GIL,应该如何处理并发
'''
from  threading import Thread
import time
def task(name):
    print('%s is runing'%name)
    time.sleep(2)
if __name__ == '__main__':
    t1 = Thread(target=task,args=('线程1',))
    t2 = Thread(target=task,args=('线程2',))
    t3 = Thread(target=task,args=('线程3',))
    # 造线程非常快，因为不用开辟空间了
    t1.start()
    t2.start()
    t3.start()
```

## 7.GILvs 自定义互斥锁

```
# 互斥锁意义在于，GIL它只是在计算型代码前后加锁，互斥锁可以在io操作前后加锁，保证数据安全
from threading import Thread,Lock
import time
n = 100
mutex=Lock()
def task():
    # 1 第一个线程抢到了GIL锁
    # 4 第二个线程抢到了第一个线程的GIL锁
    global n
    # 2 第一个线程抢到了自定义锁
    # 5 第二个线程卡在了自定义锁这里
    # 7 第二个线程抢到了第一个线程的自定义锁
    mutex.acquire()
    temp = n
    # 3 到了io只释放来GIL锁，没有释放自定义锁
    time.sleep(0.1)

    n = temp -1
    # 6 第一个线程完全的运行完自定义锁里面的代码，释放自定义锁
    mutex.release()
if __name__ == '__main__':
    t_l = []
    start = time.time()
    for i in range(100):
        t = Thread(target=task)
        t_l.append(t)
        t.start()
    for t in t_l:
        t.join()
    print(n,time.time()-start)





```

## 8.线程queue

```
# 虽然线程中数据共享，但是队列可以处理锁的问题
# import queue
# q = queue.Queue(3)
#
# q.put(1)
# q.put(2)
# q.put(3)
# print('aaa')
# # q.put(4)
# print(q.get())
# print(q.get())
# print(q.get())
# print('bbb')
# print(q.get())
from threading import Thread,active_count
import time,random
# from  multiprocessing import Process,Queue
import queue
def producer(name,food,q):
    for i in range(10):
        res = '%s%s'%(food,i)
        # 模拟生产数据的时间
        time.sleep(3)
        q.put(res)
        print('厨师%s生产了%s'%(name,res))
def consumer(name,q):
    while True:
        # 订单都没来还在等呢
        # 生产者往消费者发信号
        res = q.get()
        # 第十个是一个空
        if res is None:
            #  主线程和最后一个线程
            if active_count() is 2:
                print(time.time()-start)

            break
        # 模拟处理数据的时间
        time.sleep(3)
        print('吃货%s吃了%s' % (name, res))
if __name__ == '__main__':
    start = time.time()
    q = queue.Queue()
    # 生产者
    p1 = Thread(target=producer,args=('大海','包子',q))
    p2 = Thread(target=producer,args=('中海','辣椒炒肉',q))
    p3 = Thread(target=producer,args=('小海','土豆丝',q))
    # 消费者
    c1 = Thread(target=consumer,args=('夏洛',q))
    c2 = Thread(target=consumer,args=('西施',q))
    # 生产者和消费者并发
    p1.start()
    p2.start()
    p3.start()
    c1.start()
    c2.start()
    # 生产完了
    p1.join()
    p2.join()
    p3.join()
    # 发结束信号给消费者
    # 发送给队列一个None
    q.put(None)
    q.put(None)
    print('主')



```

## 9.多线程和多进程的应用场景

```
# 计算密集型:应该使用多进程
# from multiprocessing import Process
# from threading import Thread
# import os,time
# def work():
#     res = 0
#     for i in range(10000000):
#         res+=i
# if __name__ == '__main__':
#     l = []
#     # 查看cpu个数
#     print(os.cpu_count())
#     start = time.time()
#     for i in  range(8):
#         # 多进程8个cpu同时在算，计算效率高，但是进程之间切换效率低
#         # p = Process(target=work)
#         # 多线程是1个cpu在计算
#          # 毕竟计算效率低，但是切换效率高
#         p = Thread(target=work)
#
#         l.append(p)
#         p.start()
#     for p in l:
#         p.join()
#     print('主%s'%(time.time()-start))

# IO密集型: 应该开启多线程
from multiprocessing import Process
from threading import Thread
import os,time

def work():
    time.sleep(2)
if __name__ == '__main__':
    l= []
    start = time.time()
    for i in range(20):
        # 进程之间切换效率低
        # p = Process(target=work)
        # 毕竟计算效率低，但是切换效率高
        p = Thread(target=work)
        l.append(p)
        p.start()
    for p in l:
        p.join()
    print('主%s'%(time.time()-start))
```



## 10.tcpsocketserver服务器

```
import socketserver

class MyTCPhanler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                print('收到客户端数据',data)
                self.request.send(data.upper())
            except ConnectionResetError:
                break


if __name__ == '__main__':
    # 通信循环
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8080),MyTCPhanler)
    # 链接循环
    server.serve_forever()

```

## 10.自己写的tcp多线程（并发服务器）

```
# 客户端关闭了服务端会正常结束
# 服务端必须满足至少三点:
# 1. 绑定一个固定的ip和port
# 2. 一直对外提供服务,稳定运行
# 3. 能够支持并发,
# 因为是io密集型要开多线程

import socket
from  threading import Thread
def communicate(conn):
    # 通讯循环
    while True:
        try:
            data = conn.recv(1024)
            print('收到客户端数据',data)
            conn.send(data.upper())
        except ConnectionResetError:
            break
def server(ip,port,backlog=5):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(backlog)
    while True:
        # 链接循环
        conn,client_addr=server.accept()
        t = Thread(target=communicate,args=(conn,))
        t.start()
if __name__ == '__main__':
    s = Thread(target=server,args=('127.0.0.1',8080))
    s.start()
```