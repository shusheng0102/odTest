# 并发编程1

## 1.进程介绍

```
'''
1. 什么是进程 *****
    进程指的是一个程序的运行过程,或者说一个正在执行的程序
    所以说进程一种虚拟的概念,该虚拟概念起源操作系统
大前提:一个cpu同一时刻只能执行一个任务
    串行: 一个进程一个任务完完整整运行完毕才能执行下一个任务
            做完一件事情接着才能做下一件事
    并行: 多个任务是真正意义上的同时运行,只有多核才能实行并行
            相当于多个人在做多份工作
    并发: 多个任务看起来是同时运行的,单核下就能实现并发(并发=切换+保存状态)
        一个人做多件事，比如晚上回家，
        煮饭的时间可以切菜，炒菜，把衣服放到洗衣机，一次就做了多件事
         # 送外卖也是并发，有些外卖小哥一次接多个单
'''
```

## 2.开启进程的方式

```
from multiprocessing  import Process
import time

def task(name):
    print('%s is running'%name)
    time.sleep(3)
    print('%s is done'%name)

# 开启子进程的操作必须放到
# if __name__ == '__main__'的子代码中
# 子进程不会再次加载
if __name__ == '__main__':
    # args
    # p = Process(target=task,args=('大海',))
    # kwargs
    p = Process(target=task,kwargs={'name':'大海'})

    # print(p)
    # 主进程只是向操作系统发送了一个开启子进程的信号
    p.start()
    # 1.操作系统先申请内存空间
    # 2.把主进程的数据拷贝到子进程里面
    # 3.调用cup才能运行里面的代码
    # 创造进程的开销大
    print('主')
```

## 3.join方法等待子进程结束

```
# *****
from multiprocessing  import Process
import time

# def task(name):
#     print('%s is running'%name)
#     time.sleep(3)
#     print('%s is done'%name)
def task(name,n):
    print('%s is running'%name)
    time.sleep(n)
    print('%s is done'%name)

if __name__ == '__main__':

    # p1 = Process(target=task,args=('大海1',))
    # p2 = Process(target=task,args=('大海2',))
    # p3 = Process(target=task,args=('大海3',))
    # # 串行
    # # task('子1')
    # # task('子2')
    # # 主进程只是向操作系统发送了一个开启子进程的信号
    # p1.start()
    # p2.start()
    # p3.start()
    # # time.sleep(4)
    # # join让主进程等待子进程运行完
    # p1.join()
    # p2.join()
    # p3.join()
    # print('主')
    # 开启多个进程
    start = time.time()
    p_l = []

    for i in range(1,5):
        p = Process(target=task, args=('大海%s'%i,i))
        p_l.append(p)
        p.start()
    # # 主进程等待子进程
    for p in p_l:
        p.join()
    print('主',(time.time()-start))





```

## 4.进程之间内存空间互相隔离

```
# *****
from multiprocessing import Process

n = 100

def task():
    global n
    # 改的是子进程里面的全局变量
    # 主进程里面没有改
    n = 0

if __name__ == '__main__':
    p = Process(target=task)
    p.start()
    p.join()
    print(n)
```

## 5.进程对象其他相关的属性或方法

```
# ***
#1. 进程pid:每一个进程在操作系统内都有一个唯一的id号,称之为pid

# from multiprocessing import Process,current_process
# import time
#
# def task():
#     print('%s is running'%current_process().pid)
#     time.sleep(30)
#     print('%s is done'%current_process().pid)
# if __name__ == '__main__':
#     p = Process(target=task)
#     p.start()
#     print('主',current_process().pid)


# # os模块也可以
# from multiprocessing import Process
# import time,os
#
# def task():
#     print('%s is running爹是 %s'%(os.getpid(),os.getppid()))
#     time.sleep(30)
#     print('%s is done爹是 %s'%(os.getpid(),os.getppid()))
# if __name__ == '__main__':
#     p = Process(target=task)
#     p.start()
#     #     # 谁把主进程创造出来的
#     #     #   用pycharm就是pycharm创造的
#     print('主%s爹是 %s'%(os.getpid(),os.getppid()))


#2. 进程对象其他相关的属性或方法 （了解）
from multiprocessing import Process
import time,os

def task():
    print('%s is running爹是 %s'%(os.getpid(),os.getppid()))
    time.sleep(30)
    print('%s is done爹是 %s'%(os.getpid(),os.getppid()))
if __name__ == '__main__':
    p = Process(target=task)
    p.start()
    #     # 谁把主进程创造出来的
    #     #   用pycharm就是pycharm创造的
    # 进程的名字
    print(p.name)
    # 杀死子进程
    p.terminate()
    # 需要时间
    time.sleep(0.1)
    #  判断子进程是否存活
    print(p.is_alive())
    print('主%s爹是 %s'%(os.getpid(),os.getppid()))
```

## 6.守护进程

```
#守护进程: 本质就是一个"子进程",该"子进程"的生命周期<=被守护进程的生命周期  *****
# 主进程运行完了，子进程没有存在的意义
# 皇帝和太监不是同生，但是是同死
from multiprocessing import Process
import time

def task(name):
    print('%s活着'%name)
    time.sleep(3)
    print('%s正常死亡'%name)

if __name__ == '__main__':
    p1 = Process(target=task,args=('老太监',))
    p1.daemon = True

    p1.start()

    time.sleep(1)
    print('皇帝正在死亡')



```

## 7. 进程互斥锁

```
#  进程之间内存空间互相隔离，怎样实现共享数据 *****
# 进程之间内存数据不共享,但是共享同一套文件系统,所以访问同一个文件,是没有问题的
# 而共享带来的是竞争，竞争带来的结果就是错乱，如何控制，就是加锁处理
'''
抢票
    查票
    购票
互斥锁：
    在程序中进行加锁处理
    必须要释放锁下一个锁才能获取，所以程序在合适的时候必须要有释放锁
    如果不释放会导致程序阻塞，所以很危险。
所以用文件来处理共享数据
    1.速度慢
    2.必须有互斥锁
'''
import json
import  time,random
from multiprocessing import Process,Lock
def search(name):
    with open('db.json','rt',encoding='utf-8')as f:
        dic = json.load(f)
    # 模拟查票时间
    time.sleep(1)
    print('%s 查看到余票为%s'%(name,dic['count']))
# 第二个get子进程不会是第一个get子进程修改后count的结果
# 加互斥锁，把这一部分并发变成串行，
# 但是牺牲了效率，保证了数据安全
def get(name):
    with open('db.json','rt',encoding='utf-8')as f:
        dic = json.load(f)
        # 先看下有没有票
    if dic['count']>0:
            # 有票模拟填信息，付款，提交数据给服务端
        dic['count']-=1
        # 其他的进程全部都进来了
        time.sleep(random.randint(1,3))
        # 重新写入
        with open('db.json', 'wt', encoding='utf-8')as f:
            json.dump(dic,f)
            print('%s 购票成功'%name)
    else:
        print('%s查看到没有票了'%name)

def task(name,mutex):
    # 查票
    # 并发
    search(name)
    # 购票
    # 获取锁
    # # 串行
    mutex.acquire()
    get(name)
    # 释放锁
    mutex.release()
# if __name__ == '__main__':
#     for i in range(10):
#         p = Process(target=task,args=('路人%s'%i,))
#         p.start()
#         # 数据安全，是指读的时候无所谓，写的（改的）时候必须安全
#         # 写的时候是串行，读的时候并发
#         #  join只能将进程的任务整体变成串行
#
#         p.join()

if __name__ == '__main__':
    mutex=Lock()
    for i in range(10):
        p = Process(target=task,args=('路人%s'%i,mutex))
        p.start()
        # 数据安全，是指读的时候无所谓，写的（改的）时候必须安全
        # 写的时候是串行，读的时候并发
        #  join只能将进程的任务整体变成串行

        # p.join()
```

## 8.进程间通信(IPC机制)

```
'''
速度快  *****
锁问题解决
ipc机制
    进程彼此之间互相隔离，要实现进程间通信（IPC），
    multiprocessing模块支持两种形式：队列和管道，这两种方式都是使用消息传递的
    共享内存空间
    队列=管道+锁
'''
from multiprocessing import Queue
# 占用的内存，最好小数据，消息数据，下载地址
# Queue(限制队列里面的个数)
# 先进先出
q=Queue(3)
# 添加
q.put('a')
q.put('b')
q.put({'a':2})
print('篮子满了')
# 队列满了，相当于锁了
# q.put({'a':2})

# 提取
print(q.get())
print(q.get())
print(q.get())
# # 队列为空，等待加入，也会阻塞，相当于锁了
print('队列为空')
print(q.get())






```

## 9.生产者与消费者模型

```
'''
1. 什么是生产者消费者模型
    生产者:代指生产数据的任务
    消费者:代指处理数据的任务
    该模型的工作方式:
        生产者生产数据传递消费者处理
        实现方式:
            生产者---->队列<------消费者
        厨师----》外卖小哥和外卖平台<-----消费者
        厨师不影响生产效率               不用等厨师炒完这道菜
        可以不停的炒菜                    就可以点别的菜
        炒好的菜可以给    外卖小哥
2. 为何要用
    当程序中出现明细的两类任务,一类负责生产数据,一类负责处理数据
    就可以引入生产者消费者模型来实现生产者与消费者的解耦合,平衡生产能力与消费能力,从提升效率

3. 如何用

'''
import time,random
from  multiprocessing import Process,Queue
def producer(name,food,q):
    for i in range(10):
        res = '%s%s'%(food,i)
        # 模拟生产数据的时间
        time.sleep(random.randint(1,3))
        q.put(res)
        print('厨师%s生产了%s'%(name,res))
def consumer(name,q):
    while True:
        # 订单都没来还在等呢
        # 生产者往消费者发信号
        res = q.get()
        # 第十个是一个空
        if res is None:
            break
        # 模拟处理数据的时间
        time.sleep(random.randint(1, 3))
        print('吃货%s吃了%s' % (name, res))
if __name__ == '__main__':
    q = Queue()
    # 生产者
    p1 = Process(target=producer,args=('大海','包子',q))
    p2 = Process(target=producer,args=('中海','辣椒炒肉',q))
    p3 = Process(target=producer,args=('小海','土豆丝',q))
    # 消费者
    c1 = Process(target=consumer,args=('夏洛',q))
    c2 = Process(target=consumer,args=('西施',q))
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

## 10.JoinableQueue

```
# *****
import time,random
from  multiprocessing import Process,JoinableQueue
def producer(name,food,q):
    for i in range(10):
        res = '%s%s'%(food,i)
        # 模拟生产数据的时间
        time.sleep(random.randint(1,3))
        q.put(res)
        print('厨师%s生产了%s'%(name,res))
def consumer(name,q):
    while True:
        # 订单都没来还在等呢
        # 生产者往消费者发信号
        res = q.get()

        # 模拟处理数据的时间
        time.sleep(random.randint(1, 3))
        print('吃货%s吃了%s' % (name, res))
        # 1每次完成队列取一次，往q.join() ，取干净了q.join()运行完
        q.task_done()
if __name__ == '__main__':

    start = time.time()
    q = JoinableQueue()
    # 生产者
    p1 = Process(target=producer,args=('大海','包子',q))
    p2 = Process(target=producer,args=('中海','辣椒炒肉',q))
    p3 = Process(target=producer,args=('小海','土豆丝',q))
    # 消费者
    c1 = Process(target=consumer,args=('夏洛',q))
    c2 = Process(target=consumer,args=('西施',q))
    # #3.守护进程的作用: 主进程死了，消费者子进程也跟着死
    #     #把消费者变成守护进程
    c1.daemon = True
    c2.daemon = True
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
    # 2消费者task_done给q.join()发信号
    q.join()
    # 队列已经为空
    print('主',time.time()-start)
    # 生产者运行完？1,2
    # 消费者运行完？1,2
    # 意味着print('主')执行主进程运行完了，生产者消费者也运行完了
    # 但是消费者还是阻塞，可以用守护进程结束掉子进程
```
## 作业

```
'''
1.讲解一下守护进程是什么
2.文件来处理共享数据有什么缺点
3.生产者消费者模型敲一遍
'''
```