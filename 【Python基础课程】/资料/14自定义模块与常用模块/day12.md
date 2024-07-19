

## 模块

```
'''
1 什么是模块
    模块就是一系列功能的集合体
        模块有二种来源
            1. 自定义模块 py文件
            2. 内置的模块
        模块的格式:
            1 使用python编写的.py文件
                python文件就是一系列功能的集合体
2 为何要用模块
    1. 使用内置模块的好处是: 拿来主义,可以极大提升开发效率
    2. 使用自定义模块的好处是: 可以减少代码冗余
    (抽取我们自己程序中要公用的一些功能定义成模块,
    然后程序的各部分组件都去模块中调用共享的功能)
'''
```

## 自定义模块

#### import模块

```
# 首次导入模块发生3件事
# 1. 会产生一个模块的名称空间
# 2. 执行文件spam.py,将执行过程中产生的名字都放到模块的名称空间中
# 3. 在当前执行文件的名称空间中拿到一个模块名,该名字指向模块的名称空间

# 总结import导入模块:在使用时必须加上前缀:模块名.
# 优点: 指名道姓地向某一个名称空间要名字,肯定不会与当前名称空间中的名字冲突
# 缺点: 但凡应用模块中的名字都需要加前缀,不够简洁
```

##### from ... import ...

```
# 首次导入模块发生3件事
# 1. 创建一个模块的名称空间
# 2. 执行文件spam.py,将执行过程中产生的名字都放到模块的名称空间中
# 3. 在当前执行文件中直接拿到一个名字,该名字就是执行模块中相对应的名字的
# from 模块名  import 各种名字变量名，函数名等等

# 总结from...import...
# 优点: 使用时,无需再加前缀,更简洁
# 缺点: 容易与当前名称空间中的名字冲突


# 相对导入
# 相对导入
#         from . import 模块
#         from .. import 模块
#         from ... import 模块

# 相对导入: 参照当前所在文件的文件夹为起始开始查找,称之为相对导入
#        符号: .代表当前所在文件的文件加,..代表上一级文件夹,...代表上一级的上一级文件夹
#        优点: 导入更加简单
#        缺点: 只能在导入包中的模块时才能使用,不能在执行文件中用
# 只能在导入包中的模块时才能使用,不能在执行文件中用
# 错误
# from .dir1 import m1
#  执行文件中只能用绝对导入
```

## time模块

```
"""
    time模块
        与时间相关的功能
    在python中 时间分为3种
        1.时间戳  timestamp  从1970 年 1 月 1日 到先在的秒数  主要用于计算两个时间的差
        2.localtime  本地时间  表示的是计算机当前所在的位置
        3.UTC 世界协调时间 又称世界统一时间、世界标准时间、国际协调时间。
          时间戳 结构化 格式化字符
"""
import time
# 获取时间戳 返回的是浮点型
# 作用 用来计算时间差
print(time.time())
# 获取当地时间   返回的是结构化时间
print(time.localtime())

# 而美国部分地区还处于前日的黄昏
# 了解
# tm_wday=0, 国际的星期几  少一天
# tm_yday=165, 今年过了多少天
# tm_isdst=0  时区
#  获取UTC时间 返回的还是结构化时间  比中国时间少8小时
print(time.gmtime())
# 将获取的时间转成我们期望的格式 仅支持结构化时间
# # 结构化时间转换成字符串时间
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# 将格式化字符串的时间转为结构化时间  注意 格式必须匹配
print(time.strptime('2021-05-15 20:45:31','%Y-%m-%d %H:%M:%S'))

# 时间戳 转结构化
# 10秒时间戳
print(time.localtime(10))
# 当前时间戳
print(time.localtime(time.time()))

# 结构化转 时间戳
print(time.mktime(time.localtime()))

# sleep 
# 让当前进程睡眠一段时间 单位是秒
time.sleep(1)
print('over')
```

## datetime模块

```
"""
    datetime
        python实现的一个时间处理模块
    time 用起来不太方便  所以就有了datetime
    总结 datetime相比time 更灵活 更本土化
"""
# import datetime
#
# print(datetime.datetime.now())

from datetime import datetime
# 获取时间 获取当前时间 并且返回的是格式化字符时间
print(datetime.now())
# 单独获取某个时间 年 月
d=datetime.now()
print(d.year)
print(d.month)
print(d.day)
print(d.minute)
print(d.second)
print(d.microsecond)

# 手动指定时间
print(datetime(2018,8,9,9,50,00))
d2=datetime(2018,8,9,9,50,00)
print(d-d2)
# 替换某个时间单位的值
print(d.replace(year=2019))
```

## hash模块

```
# 1、什么叫hash:hash是一种算法，该算法接受传入的内容，经过运算得到一串hash值
# 2、hash值的特点是：
#2.1 只要传入的内容一样，得到的hash值必然一样=====>文件完整性校验
#2.2 不能由hash值返解成内容=======》把密码做成hash值，不应该在网络传输明文密码
#2.3 只要使用的hash算法不变，无论校验的内容有多大，得到的hash值长度是固定的,这样不影响传输

import hashlib
# # 1创建hash工厂
# m=hashlib.md5()
# # 运输的是二进制
# # 2在内存里面运送
# # m.update('helloworld'.encode('utf-8'))
# # 一点一点的给，因为可能二进制会很长 ,这个要好一些
# m.update('hello'.encode('utf-8'))
# m.update('world'.encode('utf-8'))
#
# # 3、产出hash值
# print(m.hexdigest())
# 'fc5e038d38a57032085441e7fe7010b0'

# m = hashlib.md5()
# with open(r'D:\python代码1\day10\基础继承.png','rb')as f:
#     for line in f:
#         m.update(line)
#     hv = m.hexdigest()
# print(hv)
# 输入密码的时候是沿着网络传输到别的服务器上面，黑客可以把包抓下来
# 所以发给服务端是hash值，也就是密文
# 但是还是可以抓下来
# 常用密码字典
# 什么生日 ， 123 ， 身份证  等等 密码有强烈的个人习惯
# 那么我用一样的hash算法，是不是可以得到一样的hash值  密文  那么明文肯定是一样的
# 撞库风险

# 密码前后加盐
# import  hashlib
# pwd = 'abc123'
# m = hashlib.md5()
# m.update('大海老师大帅比'.encode('utf-8'))
# m.update(pwd.encode('utf-8'))
# m.update('夏洛特烦恼'.encode('utf-8'))
# print(m.hexdigest())
# 服务器也有相应的规则
# 黑客破解成本远大于收益成本

# 中间加盐

# import  hashlib
# pwd = 'abc123'
# print(pwd[0])
# print(pwd[1:])
# m = hashlib.md5()
# m.update('大海老师大帅比'.encode('utf-8'))
# m.update(pwd[0].encode('utf-8'))
# m.update('夏洛特'.encode('utf-8'))
# m.update(pwd[1:].encode('utf-8'))
# m.update('烦恼'.encode('utf-8'))
# print(m.hexdigest())

#只要使用的hash算法不变， hash值长度是固定的

import hashlib
m=hashlib.md5()
m.update('helloaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))
print(m.hexdigest())
# 5d41402abc4b2a76b9719d911017c592
# sha后面的数字越大加密的算法越复杂
m1=hashlib.sha256()
m1.update('helloaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))
print(m1.hexdigest())
# f683dd28f66cd8b5042b66b39c192e93485d98a80f7ae8e04924b378b96ff4ea

m2=hashlib.sha512()
m2.update('helloaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))
print(m2.hexdigest())
```

## base64模块

```
'''
Base64是网络上最常见的用于传输8Bit字节码的编码方式之一，
Base64就是一种基于64个可打印字符来表示二进制数据的方法。
定义     8Bit字节代码的编码方式之一
可用于    在HTTP环境下传递较长的标识信息
特性      Base64编码具有不可读性
# 它只是用传输，并不是加密
 Base64编码原理
    看一下Base64的索引表，字符选用了"A-Z、a-z、0-9、+、/" 64个可打印字符。
    数值代表字符的索引，这个是标准Base64协议规定的，不能更改。
'''
import base64

a= '大海'
a = a.encode('utf-8')
# # 想将字符串转编码成base64,要先将字符串转换成二进制数据
str_a=base64.b64encode(a)
print(str_a)
# 可以理解成一个中介
# 将base64解码成字符串

str_b=base64.b64decode(str_a).decode('utf-8')
print(str_b)



```

## json序列化

```
'''
# 什么是变量?
#变量即变化的量，核心是“变”与“量”二字，变即变化，量即衡量状态。
# 为什么要有变量?
#程序执行的本质就是一系列状态的变化，变是程序执行的直接体现，
# 所以我们需要有一种机制能够反映或者说是保存下来程序执行时状态以及状态的变化。
# 01 什么是序列化/反序列化
#     我们把对象(变量)从内存中变成可存储或传输的过程称之为序列化
#     序列化就是将内存中的数据结构转换成一种中间格式存储到硬盘或者基于网络传输
#     反序列化就是硬盘中或者网络中传来的一种数据格式转换成内存中数据结构
# 02 为什要有
#     1、可以保存程序的运行状态
#     2、数据的跨平台交互
常用方法
        序列化
            dumps  处理字符串
            dump   处理文件

        反序列化
            loads 处理字符串
            load  处理文件

'''
import json
dic = {'name':'dahai','age':18,'sex':'man'}
#序列化：内存中的数据类型------>中间格式json
# dumps(数据类型)
# # # 1、序列化得到json_str
# json_str=json.dumps(dic)
# print(json_str)
# # # 2、把json_str写入文件
# with open('db.json','wt',encoding='utf-8')as f:
#     f.write(json_str)
# #1和2合为一步
# dump(数据类型,文件对象)
with open('db1.json','wt',encoding='utf-8')as f:
    json.dump(dic, f)




```

## json反序列化

```
import json
# 反序列化
#             loads 处理字符串
#             load  处理文件
#反序列化：中间格式json-----》内存中的数据类型
# loads(json格式字符串)
# #1、从文件中读取json_str
with open('db.json','rt',encoding='utf-8')as f:
    json_str=f.read()
    print(json_str)
# #2、将json_str转成内存中的数据类型
    dic=json.loads(json_str)
    print(dic,type(dic))
    
# load(json文件对象)
#1和2可以合作一步
with open('db.json','rt',encoding='utf-8')as f:
    dic=json.load(f)
    print(dic)



```

## os模块

```
"""
    OS模块
        os表示操作系统相关
        os模块是与操作系统交互的一个接口
        就是围绕文件和目录的操作

"""
# 工作目录，当前目录，父级目录都是一个day12
import os
# 获取当前工作目录，绝对路径
print(os.getcwd())
# 生成目录
# os.mkdir('dirname1')
# 空目录，若目录不为空则无法删除
# os.rmdir('dirname1')

# os.mkdir('dirname')
# os.rmdir('dirname')
# 拿到当前脚本工作的目录，相当于cd
# os.chdir('dirname')
# # 删除文件
# os.remove('a1.py')
# os.rmdir('dirname')
# 可生成多层递归目录
# os.makedirs('dir1/dir2/dir3/dir4')
# os.removedirs('dir1/dir2/dir3/dir4')

# os.makedirs('dir1/dir2/dir3/dir4')
# 在dir2下面创建一个文件，会产生保护机制只删除到dir2
# os.removedirs('dir1/dir2/dir3/dir4')

# 拿到当前文件夹的文件名或者文件夹放入列表
# 绝对路径
print(os.listdir(r'D:\python代码1\day12'))
# 相对路径
print(os.listdir('.'))
# 上一级
print(os.listdir('..'))
# 重命名文件/目录

# os.rename('oldname','newname')
# 运行终端命令

# os.system('tasklist')


# os.path 下面的方法  path是路径
# 将path分割成目录和文件名二元组返回
print(os.path.split('/a/b/c/d.txt'))
# 文件夹
print(os.path.split('/a/b/c/d.txt')[0])
# 文件
print(os.path.split('/a/b/c/d.txt')[1])
#返回path的目录。其实就是os.path.split(path)的第一个元素
print(os.path.dirname('/a/b/c/d.txt'))
# 返回path最后的文件名。即os.path.split(path)的第二个元素
print(os.path.basename('/a/b/c/d.txt'))
# 判断路径是否存在 文件和文件夹都可以 如果path存在，返回True；如果path不存在，返回False
print(os.path.exists('D:\python代码1\day12'))
print(os.path.exists('D:\python代码1\da'))
print(os.path.exists(r'D:\python代码1\day12\4.hash模块.py'))
# 如果path是一个存在的文件，返回True。否则返回False
print(os.path.isfile(r'D:\python代码1\day12\4.hash模块.py'))
print(os.path.isfile(r'D:\python代码1\day12\4.has块.py'))
# 也可以用相对路径
print(os.path.exists(r'./4.hash模块.py'))
print(os.path.exists(r'../day12/4.hash模块.py'))
# 如果path是一个存在的目录，则返回True。否则返回False
print(os.path.isdir('D:\python代码1\day12'))
print(os.path.isdir('D:\python代码1\da'))
# 拼接一个绝对路径，会忽略前面的路径
print(os.path.join('a','b','c','D:\\','f','d.txt'))
print(os.path.join('D:\\','f','d.txt'))
```

## random模块

```
"""
    random 随机数相关模块

"""
import random
# 0 - 1 随机浮点 不包含1 random 0-1 开闭
print(random.random())
# randint 1 - 3 开开 整型
print(random.randint(1,3))
# randrange 1 - 3 开闭
print(random.randrange(1,3))
# 随机选⼀个
print(random.choice([1,2,3]))

# 随机选指定个数sample(列表，指定列表的个数)
print(random.sample([1,2,3],2))

# 打乱顺序shuffle(列表)
l= [2,3,4,5,6]
random.shuffle(l)
print(l)
# 闭闭 浮点
print(random.uniform(1,2))
print(random.uniform(1,3))

# 作业
# 生产验证码函数 整形和字母大小写随机组成  可以指定长度
```

## sys模块

```
"""
    sys模块
    sys模块是与python解释器交互的一个接口
"""
import sys
# sys.path   返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值
print(sys.path)
sys.path.append('D:\python代码1\day12\dir0')
print(sys.path)
from dir2 import aaaaa

aaaaa.a()
```