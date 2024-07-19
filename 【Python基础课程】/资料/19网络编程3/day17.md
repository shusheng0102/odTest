# 网络编程3

## 1.进程池和线程池

```
'''
计算机开进程或者线程受限于计算机本身的硬件，所以就有了进程池和线程池限制最大进程或者线程数
不会造新的进程或者线程，不会浪费内存空间
'''
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time,os,random
def task(name):
    print('%s%s is running'%(name,os.getpid()))
    time.sleep(random.randint(1,3))
    return 123
if __name__ == '__main__':
    # print(os.cpu_count())
    p=ProcessPoolExecutor(4)
    # 只会开4个进程的id
    # p.submit(task,'进程的pid')
    # p.submit(task,'进程的pid')
    # p.submit(task,'进程的pid')
    # p.submit(task,'进程的pid')
    # # # 节约了再次开辟进程空间
    # p.submit(task,'进程的pid')
    # p.submit(task,'进程的pid')
    # for i in range(20):
    #     # p.submit(task,'进程的pid')
    #     # 返回值
    #     future=p.submit(task, '进程的pid')
    #
    #     # print(future)
    #     # 同步调用
    #     print(future.result())
    # print('主')
#     异步
    l = []
    for i in range(10):
        # p.submit(task,'进程的pid')
        # 返回值
        future=p.submit(task, '进程的pid')

        # print(future)
        l.append(future)
    # #关闭进程池的入口,并且在原地等待进程池内所有任务运行完毕
    p.shutdown(wait=True)
    for future in l:
        # 一次性全部拿到结果
        print(future.result())
    print('主')



'''
提交任务的两种方式:
同步调用:提交完一个任务之后,就在原地等待,等待任务完完整整地运行完毕拿到结果后,再执行下一行代码,会导致任务是串行执行的
提交任务的方法，串行是任务的运行状态
异步调用:提交完一个任务之后,不在原地等待,结果???,而是直接执行下一行代码,会导致任务是并发执行的

'''





```

## 2.异步解耦合

```
# from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
# import time,os,random
# # 模拟下载
# # 谁闲下来了谁去解析
# def get(i):
#     print('%s 下载进程 %s'%(os.getpid(),i))
#     time.sleep(3)
#     # 调用解析
#     parse(i)
# # 模拟解析
# def parse(i):
#     print('%s 解析进程结果为%s'%(os.getpid(),i))
#     time.sleep(1)
#
# if __name__ == '__main__':
#     p = ProcessPoolExecutor(9)
#     start = time.time()
#     for i in range(9):
#         future = p.submit(get,i)
#     p.shutdown(wait=True)
#     print('主',time.time()-start)
#     print('主',os.getpid())
# 这样get和parse耦合在一起
# 怎样实现解耦合
#
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time,os,random
# 模拟下载
# 谁闲下来了谁去解析
# def get(i):
#     print('%s 下载进程 %s'%(os.getpid(),i))
#     time.sleep(random.randint(1,3))
#     # 调用解析
#     # parse(i)
#     return i
# # 模拟解析
# def parse(i):
#     i = i.result()
#     print('%s 解析进程结果为%s'%(os.getpid(),i))
#     time.sleep(1)
#
# if __name__ == '__main__':
#     p = ProcessPoolExecutor(9)
#     start = time.time()
#     for i in range(9):
#         future = p.submit(get,i)
#         # 添加一个任务回收
#         # 异步的9个进程会闲下来，闲下来的时候去做parse这个函数里面的事情
#         future.add_done_callback(parse)
#         #  parse会在任务运行完毕后自动触发,然后接收一个参数future对象
#         #         # 主进程处理解析，解析时间短，没必要去等下载完，由主进程一个(人)搞定
#         #         # 其他子进程专心下载
#     p.shutdown(wait=True)
#     print('主',time.time()-start)
#     print('主',os.getpid())

# io密集型,线程来做
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time,os,random
from threading import current_thread
# 模拟下载
# 谁闲下来了谁去解析
def get(i):
    print('%s 下载线程 %s'%(current_thread().name,i))
    time.sleep(random.randint(1,3))
    # 调用解析
    # parse(i)
    return i
# 模拟解析
def parse(i):
    i=i.result()
    print('%s 解析进程结果为%s'%(current_thread().name,i))
    time.sleep(1)

if __name__ == '__main__':
    p = ThreadPoolExecutor(9)
    start = time.time()
    for i in range(9):
        future = p.submit(get,i)
        # 添加一个任务回收
        #         # 异步的9个线程会闲下来，闲下来的时候去做parse这个函数里面的事情
        future.add_done_callback(parse)
        # 异步调用:提交完一个任务之后,不在原地等待,而是直接执行下一行代码,
        #         # 会导致任务是并发执行的,,结果futrue对象会在任务运行完毕后自动传给回调函数
        #         #  parse会在任务运行完毕后自动触发,然后接收一个参数future对象
        #         # 那一个线程先结束下载就去处理解析，解析时间短，没必要去等其他线程下载完
    p.shutdown(wait=True)
    print('主',time.time()-start)
    print('主',current_thread().name)











```

## 3.协程

```
'''
在线程下实现并发
    操作系统认为最小单位是线程
    并发(多个任务看起来是同时执行就是并发):切换+保存状态（操作系统）
    多线程是多个线程，线程在一个进程里面，线程之间切换，整个程序
    多进程其实也是多个线程，线程分散到不同进程里面了，进程之间切换，整个程序
    线程遇到io阻塞
    应用程序级别来控制切换多个任务
    遇到io操作切换才有意义
协程
    协程是单线程实现并发，又称微线程
    注意:协程是程序员想象出来的东西,操作系统里只有进程和线程的概念(操作系统调度的是线程)
    在单线程下实现多个任务间遇到IO就切换就可以降低单线程的IO时间,从而最大限度地提升单线程的效率
    没有遇到io切换会降低效率
    遇到io切换会增加效率
    链接循环和通信循环，并没有解决单线程下的io问题
    协程可以把单个线程的效率最高
'''
```

## 4.gevent

```
# 安装模块  pip install gevent
# 1.必须要放到文件的开头
# 打标记
from gevent import monkey
# 所有的io行为进行打包
monkey.patch_all()
# 导入gevent管理的任务
from gevent import spawn,joinall
import time
def play(name):
    print('%s play 1'%name)
    time.sleep(5)
    print('%s play 2'%name)

def eat(name):
    print('%s eat 1'%name)
    time.sleep(3)
    print('%s eat 2'%name)

start = time.time()
# 异步提交任务,不管结果，直接运行下行代码
g1=spawn(play,'大海1')
g2=spawn(play,'大海2')
# g1.join()
# g2.join()
# 一行代码搞定
joinall([g1,g2])
# time.sleep(4)
# 线程死了没了
print('主',time.time()-start)



```

## 5.单线程实现并发的套接字通信

### 服务器

```
# 客户端关闭了服务端会正常结束
# 服务端必须满足至少三点:
# 1. 绑定一个固定的ip和port
# 2. 一直对外提供服务,稳定运行
# 3. 能够支持并发,
# 因为是io密集型要开多线程
# 打标记
from gevent import monkey
# 所有的io行为进行打包
monkey.patch_all()
# 导入gevent管理的任务
from gevent import spawn,joinall
import socket

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
        spawn(communicate,conn)

if __name__ == '__main__':
    # 链接循环任务提交
    s = spawn(server,'127.0.0.1',8080)
    # 链接等待结束，是一个死循环任务不会结束
    s.join()
```

### 客户端

```
from  threading import Thread,current_thread
from socket import *

def client():
    client = socket(AF_INET,SOCK_STREAM)
    client.connect(('127.0.0.1',8080))
    n = 0
    while True:
        msg = '%s say hello %s'%(current_thread().name,n)
        n += 1
        client.send(msg.encode('utf-8'))
        data = client.recv(1024)
        print(data.decode('utf-8'))

if __name__ == '__main__':
    for i in range(500):

        t = Thread(target=client)
        t.start()
```

## 6.pycharm连接虚拟机

```
# pycharm连接虚拟机
# 1 我用虚拟机上面的python软件
# # pycharm运行虚拟机里面的py文件，文件交互
# # 可以把pycharm的文件上传到虚拟机，也可以把虚拟机的文件下载到
```