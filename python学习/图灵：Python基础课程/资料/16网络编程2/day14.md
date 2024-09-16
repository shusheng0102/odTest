### 网络编程2.tcp套接字与udp套接字

#### 1.基于tcp套接字通信循环

##### 服务端

```
import socket

# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.插手机卡
phone.bind(('127.0.0.1',8080))
# 3开机
phone.listen(5)

# 4等待电话请求
print('start')
# # 建立三次握手
conn,client_addr=phone.accept()
# # 建立三次握手后的套接字
print(conn)
# 客户端的ip和端口
print(client_addr)

#5 收/发消息
#1024接收的最大字节数bytes
while True:
    # 客户端已经关闭，非正常断开来链接，服务端在用没有意义的conn，recv
    # 数据从客户端网线》》服务端网卡》》服务端操作系统 》》
    # 客户端关闭直接抛出异常 用try捕获
    try:
        data = conn.recv(1024)
        print('收到客户端的数据',data)
        # 变大写发送回去
        conn.send(data.upper())
    except ConnectionResetError:
        break
# 6挂电话链接
conn.close()

# 7关机
phone.close()









```

##### 客户端

```
import socket

# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.拨号
phone.connect(('127.0.0.1',8080))

# 3.发/收消息
# 必须传入二进制，
# 物理层
while True:
    msg = input('>>.').strip()
    if len(msg) == 0:continue
    phone.send(msg.encode('utf-8'))

    # 收
    data = phone.recv(1024)
    print('收到服务端的数据',data)


# 4关机
phone.close()
```

#### 2.基于tcp套接字链接循环+通信循环

##### 服务端

```
# *****

import socket

# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.插手机卡
phone.bind(('127.0.0.1',8080))
# 3开机
# 等待连接的客户端
phone.listen(5)

# 4等待电话请求
print('start')
# # 建立三次握手
while True:
    conn,client_addr=phone.accept()
    # # 建立三次握手后的套接字
    print(conn)
    # 客户端的ip和端口
    print(client_addr)

    #5 收/发消息
    #1024接收的最大字节数bytes
    while True:
        # 客户端已经关闭，非正常断开来链接，服务端在用没有意义的conn，recv
        # 数据从客户端网线》》服务端网卡》》服务端操作系统 》》
        # 客户端关闭直接抛出异常 用try捕获
        try:
            data = conn.recv(1024)
            print('收到客户端的数据',data)
            # 变大写发送回去
            conn.send(data.upper())
        except ConnectionResetError:
            break
    # 6挂电话链接
    conn.close()

# 7关机
phone.close()









```

##### 客户端

```
import socket

# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.拨号
phone.connect(('127.0.0.1',8080))

# 3.发/收消息
# 必须传入二进制，
# 物理层
while True:
    msg = input('>>.').strip()
    if len(msg) == 0:continue
    phone.send(msg.encode('utf-8'))

    # 收
    data = phone.recv(1024)
    print('收到服务端的数据',data)


# 4关机
phone.close()
```

#### 3.模拟实现远程命令

##### subprocess

```
'''
1. 什么是进程
    进程指的是一个程序的运行过程,或者说一个正在执行的程序
    所以说进程一种虚拟的概念,该虚拟概念起源操作系统
subprocess模块
    sub   子
    process  进程
        正在进行中的程序   每当打开一个程序就会开启一个进程
        每个进程包含运行程序所需的所有资源
        正常情况下 不可以跨进程访问数据  qq不能访问微信，微信不能访问qq
        但是有些情况写就需要访问别的进程数据    美团跳转到支付宝  这里跨进程了
        提供一个叫做管道的对象 专门用于跨进程通讯
    作用:用于执行系统命令
    总结  subprocess的好处是可以获取指令的执行结果

'''
import subprocess
cmd = input('输入命令')
        # shell：如果该参数为 True，
        # 将通过操作系统的 shell 执行指定的命令。
        # PIPE开启了一座桥，在2个进程之间
        # 命令stdout正确输出的结果
        # 命令stderr错误输出的结果
obj=subprocess.Popen(cmd,
                 shell=True,
                 stdout= subprocess.PIPE,
                 stderr= subprocess.PIPE,
                 )
stdout=obj.stdout.read().decode('gbk')
stderr=obj.stderr.read().decode('gbk')
print(stdout+stderr)


















```

##### 服务端

```
import socket
import subprocess
# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.插手机卡
phone.bind(('127.0.0.1',8080))
# 3开机
# 等待连接的客户端
phone.listen(5)

# 4等待电话请求
print('start')
# # 建立三次握手
while True:
    conn,client_addr=phone.accept()
    # # 建立三次握手后的套接字
    print(conn)
    # 客户端的ip和端口
    print(client_addr)

    #5 收/发消息
    #1024接收的最大字节数bytes
    while True:
        # 客户端已经关闭，非正常断开来链接，服务端在用没有意义的conn，recv
        # 数据从客户端网线》》服务端网卡》》服务端操作系统 》》
        # 客户端关闭直接抛出异常 用try捕获
        try:
            cmd = conn.recv(1024)

            # shell：如果该参数为 True，
            # 将通过操作系统的 shell 执行指定的命令。
            # PIPE开启了一座桥，在2个进程之间
            # 命令stdout正确输出的结果
            # 命令stderr错误输出的结果
            obj = subprocess.Popen(cmd.decode('utf-8'),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   )
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            print(len(stdout + stderr))
            conn.send(stdout + stderr)
            # 先发给自己的操作系统,保存在自己的操作系统里面,堆积在这里
        except ConnectionResetError:
            break
    # 6挂电话链接
    conn.close()

# 7关机
phone.close()
# 客户端关闭了服务端会正常结束
# 服务端必须满足至少三点:
# 1. 绑定一个固定的ip和port
# 2. 一直对外提供服务,稳定运行
# 3. 能够支持并发,
# 因为是io密集型要开多线程








```

##### 客户端

```
import socket

# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.拨号
phone.connect(('127.0.0.1',8080))

# 3.发/收消息
# 必须传入二进制，
# 物理层
while True:
    msg = input('>>.').strip()
    if len(msg) == 0:continue
    phone.send(msg.encode('utf-8'))

    # 收
    data = phone.recv(1024)
    print('收到服务端的数据',data.decode('gbk'))


# 4关机
phone.close()
```

#### 4.粘包问题分析

##### 服务端

```
import socket
import subprocess
import struct
# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.插手机卡
phone.bind(('127.0.0.1',8080))
# 3开机
# 等待连接的客户端
phone.listen(5)

# 4等待电话请求
print('start')
# # 建立三次握手
while True:
    conn,client_addr=phone.accept()
    # # 建立三次握手后的套接字
    print(conn)
    # 客户端的ip和端口
    print(client_addr)

    #5 收/发消息
    #1024接收的最大字节数bytes
    while True:
        # 客户端已经关闭，非正常断开来链接，服务端在用没有意义的conn，recv
        # 数据从客户端网线》》服务端网卡》》服务端操作系统 》》
        # 客户端关闭直接抛出异常 用try捕获
        try:
            cmd = conn.recv(1024)

            # shell：如果该参数为 True，
            # 将通过操作系统的 shell 执行指定的命令。
            # PIPE开启了一座桥，在2个进程之间
            # 命令stdout正确输出的结果
            # 命令stderr错误输出的结果
            obj = subprocess.Popen(cmd.decode('utf-8'),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   )
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            # print(len(stdout + stderr))
            # conn.send(stdout + stderr)
            # 先发给自己的操作系统,保存在自己的操作系统里面,堆积在这里     #            # 一. 获得数据长度  ******
            header_long=len(stdout + stderr)
            # # 二. 先制作固定长度的报头
            header=struct.pack('i',header_long)
            # # 三. 再发送报头
            conn.send(header)
            # # 四. 最后发送真实的数据
            conn.send(stdout + stderr)

        except ConnectionResetError:
            break
    # 6挂电话链接
    conn.close()

# 7关机
phone.close()
# 客户端关闭了服务端会正常结束
# 服务端必须满足至少三点:
# 1. 绑定一个固定的ip和port
# 2. 一直对外提供服务,稳定运行
# 3. 能够支持并发,
# 因为是io密集型要开多线程








```

##### 客户端

```
import socket
import struct
# 1买手机
# AF_INET 互联网协议
# SOCK_STREAM TCP流式协议,
phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print(phone)

# 2.拨号
phone.connect(('127.0.0.1',8080))

# 3.发/收消息
# 必须传入二进制，
# 物理层
while True:
    msg = input('>>.').strip()
    if len(msg) == 0:continue
    phone.send(msg.encode('utf-8'))

    # 收
    # 五.先收报头
    header = phone.recv(4)
    # 六.从报头里解出真实数据的长度
    total_size=struct.unpack('i',header)[0]
    # 七. 接收真正的数据
    # 一次性接收好不好
    cmd_res = b''
    resv_size = 0
    while resv_size < total_size:
        # 假设是1024以下就一次接受完了
        # 如果大于1024是不是要多次
        # 可以把recv想象成一个袋子
        # 一次只能转1024
        data = phone.recv(1024)
        resv_size += len(data)
        cmd_res += data


    # data = phone.recv(total_size)
    print('收到服务端的数据',cmd_res.decode('gbk'))


# 4关机
phone.close()
```

##### struct

```
# 把整型数字转换成固定长度的Bytes类型 ***
import struct
# 把数字转换成4个Bytes
obj1 = struct.pack('i',1000000)

print(obj1,len(obj1))

res1 = struct.unpack('i',obj1)

print(res1)
print(res1[0])
print(type(res1[0]))
```

#### 5.基于udp协议通信的套接字

##### 服务端

```
# 没有实现真正意义的并发
# 只是说收发消息很快
# 原因是由于数据量太小
# 客户端太少

import socket
# udp用SOCK_DGRAM数据报
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('127.0.0.1',8080))


while True:
    # 接收的是数据和客户端的ip和端口元组
    data,client_addr=server.recvfrom(1024)
    print(data)
    print(client_addr)
    server.sendto(data.upper(),client_addr)
```

##### 客户端

```
import socket
# udp用SOCK_DGRAM数据报
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    msg = input('>>>').strip()
    # 爱收就收，不收也会把操作系统数据清清除
    client.sendto(msg.encode('utf-8'),('127.0.0.1',8080))
    # 发空也可以，因为报头有数据
    data,server_addr = client.recvfrom(1024)
    print(data)
```

##### 服务端测试

```
# 没有实现真正意义的并发
# 只是说收发消息很快
# 原因是由于数据量太小
# 客户端太少
import time
import socket
# udp用SOCK_DGRAM数据报
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('127.0.0.1',8080))


while True:
    # 接收的是数据和客户端的ip和端口元组
    data,client_addr=server.recvfrom(1024)
    print(data)
    print(client_addr)
    time.sleep(3)
    server.sendto(data.upper(),client_addr)
```

##### 客户端直接传输

```
import socket
import time
# udp用SOCK_DGRAM数据报
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
i = 0
while True:
    i += 1
    # 爱收就收，不收也会把操作系统数据清清除
    client.sendto(('helloa%s'%i).encode('utf-8'),('127.0.0.1',8080))
    # 发空也可以，因为报头有数据
    time.sleep(2)
    data,server_addr = client.recvfrom(1024)
    print(data)
```

##### socketserver模块实现多线程udp并发服务端

```
import socketserver
import time

class MyUphander(socketserver.BaseRequestHandler):
    def handle(self):
        # 数据和套接字
        # print(self.request)
        data,sock=self.request
        print(data)
        time.sleep(1)
        sock.sendto(data.upper(),self.client_address)



if __name__ == '__main__':
    # 1.创建一个线程的通信循环
    server = socketserver.ThreadingUDPServer(('127.0.0.1',8080),MyUphander)
    # 链接循环 serve_forever永远提供服务
    server.serve_forever()
```

#### 6.数据报协议的特点

##### 服务端

```
# tcp协议可能是多发对应一收    数据流 *****
# 优点，传输数据更加可靠
# 缺点，每次传数据必须建立链接，每次发数据必须确认
# 下载，转载用tcp
# udp是一发对应一收 ，不会有粘包问题，数据报
# 稳定传输的字节512字节
# 优点，传输数据更快
# 缺点，数据容易丢失， 传输数据不可靠
# 用于聊天udp

import socket
# udp用SOCK_DGRAM数据报
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('127.0.0.1',8080))

# 没有任何粘包问题
print(server.recvfrom(1024))
print(server.recvfrom(1024))
```

##### 客户端

```
import socket
# udp用SOCK_DGRAM数据报
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

client.sendto(b'hello',('127.0.0.1',8080))
client.sendto(b'world',('127.0.0.1',8080))
client.sendto(b'world',('127.0.0.1',8080))
client.sendto(b'world',('127.0.0.1',8080))
client.sendto(b'world',('127.0.0.1',8080))
client.sendto(b'world',('127.0.0.1',8080))
```

##### 作业

```
'''
1.讲解一些tcp和udp的区别
2.模拟实现远程执行命令敲一遍
记得一定要在settings里面导入模块 requests  pyquery
'''
```