# day6字符编码与文件操作

### 1.字符编码

```
'''
一 什么是字符编码?
计算机要想工作必须通电,即用‘电’驱使计算机干活,也就是说‘电’的特性决定了计算机的特性。
电的特性即高低电平(人类从逻辑上将二进制数1对应高电平,二进制数0对应低电平)
    简单来说就是一个灯泡亮一个灯泡不亮表示
        0代表灯泡不亮 (低电平)
        1代表灯泡亮  （高电平）
        那么2个灯泡可以表示的信息就有  00 01 10 11 4种 2的二次方
        那么3个灯泡可以表示的信息就有  000 001  100 010  110 101 011 111 8种  二的三次方
    结论：计算机只认识数字(二进制0101) 其他的数字10进制是通过二进制转换过来的
         很明显，我们平时在使用计算机时，用的都是人类能读懂的字符
        （用高级语言python编程的结果也无非是在文件内写了一堆字符），
        如何能让计算机读懂人类的字符？
        必须经过一个过程：
        #字符--------（翻译过程）------->数字
        #这个过程实际就是一个字符如何对应一个特定数字的标准，这个标准称之为字符编码
    字符编码的发展史与分类？
        计算机由美国人发明。
            英文编码
            ASCII   ascii用1个字节（8位二进制）代表一个二进制字符   01010100
                 8bit= 1Bytes
                1024Bytes=1KB
                1024KB=1MB
                1024MB=1GB
                1024GB=1TB
                1024TB=1PB
             最早的字符编码为ASCII，只规定了英文字母数字和一些特殊字符与数字的对应关系。
            一个字节  01010100
             所以，ASCII码最多只能表示 256 个符号。即：2**8 = 256，
             当然我们编程语言都用英文(python,java)没问题，ASCII够用，但是在处理数据时，
                    不同的国家有不同的语言，日本人会在自己的程序中加入日文，中国人会加入中文。
                    比如print('中文') python3自动设置好的  之前python2需要设置
                    ASCII无法表示中文
                        而要表示中文，单拿一个字节表表示一个汉子，是不可能的
                        中国文化博大精深
                        是不可能表达完的(连小学生都认识两千多个汉字)，
                        多个字节去表示
                        位数越多，代表的变化就多，这样，就可以尽可能多的表达出不同的汉字
            gb2312
                所以中国人规定了自己的标准gb2312编码，
                规定了包含中文在内的字符－>数字的对应关系。
            GBK的诞生   3个字节  01010100 01010100 01010100  2**24
                GB 2312的出现，基本满足了汉字的计算机处理需要，
                但对于人名、古汉语等方面出现的罕用字，GB 2312不能处理，
                这导致了后来GBK汉字字符集的出现。
            Shift_JIS
                日本人规定了自己的Shift_JIS编码
            Euc-kr
                韩国人规定了自己的Euc-kr编码
                （另外，韩国人说，
                要求世界统一用韩国编码，但世界人民没有搭理他们）
                原因 ：政治
            unicode的诞生 它是在内存里面的
                unicode常用2个字节（16位二进制）代表一个字符，生僻字需要用4个字节（32位二进制）
                这时候问题出现了，精通18国语言的 某某大海 谦虚的用8国语言写了一篇文档，
                那么这一篇文档，按照哪国的标准，都会出现乱码（因为此刻的各种标准都只是
                规定了自己国家的文字在内的字符跟数字的对应关系，如果单纯采用一种国家的编码格式，
                那么其余国家语言的文字在解析时就会出现乱码）
                所以迫切需要一个世界的标准（能包含全世界的语言）
                于是unicode应运而生（韩国人表示不服，然后没有什么卵用）
                    字母x，用unicode表示二进制0000 0000 0111 1000，所以unicode兼容ascii，也兼容万国
                    这时候乱码问题消失了，所有的文档我们都使用但是新问题出现了，如果我们的文档通篇都是英文，
                    你用unicode会比ascii耗费多一倍的空间，在存储和传输上十分的低效
            UTF-8的诞生  它是在硬盘里面的
                 本着节约的精神 又出现了把Unicode编码转化为“可变长编码”的UTF-8编码。
                UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，
                    汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。
                    字符	    ASCII	         Unicode	                     UTF-8
                    A	    01000001	      00000000 01000001	             01000001
                    中	    没有	             11100100 01001110 00101101	     11100100 10111000 10101101
                    简单来说英文字母 UTF-8 使用的和 ASCII 对应关系 一样
                                而中文 UTF-8 使用 Unicode 对应关系
            unicode和UTF-8的关系
                1、在存入磁盘时，需要将unicode转成一种更为精准的格式，
                utf-8:全称Unicode Transformation Format，将数据量控制到最精简
                2、在读入内存时，需要将utf-8转成unicode
                所以我们需要明确：内存中用unicode是为了兼容万国软件，
                即便是硬盘中有各国编码编写的软件，unicode也有相对应的映射关系，
                但在现在的开发中，程序员普遍使用utf-8编码了，
                估计在将来的某一天等所有老的软件都淘汰掉了情况下，
                就可以变成：内存unicode<->硬盘utf-8的形式了。
'''











```

### 2.文件操作

```
'''
1 什么是文件
    文件是操作系统为用户/应用程序提供的一种操作硬盘的抽象单位
2 为何要用文件
    用户/应用程序对文件的读写操作会由操作系统转换成具体的硬盘操作
    所以用户/应用程序可以通过简单的读\写文件来间接地控制复杂的硬盘的存取操作
    实现将内存中的数据永久保存到硬盘中

    user=input('>>>>: ') #user="大海"
3 如何用文件
    文件操作的基本步骤:
        f=open(...) #打开文件,拿到一个文件对象f,f就相当于一个遥控器,可以向操作系统发送指令
        f.read() # 读写文件,向操作系统发送读写文件指令
        f.close() # 关闭文件,回收操作系统的资源
    上下文管理:
        with open(...) as f:
            pass
'''
# 绝对路径
# f = open(r'D:\python代码2\day7\a.txt',encoding='utf-8')
# f1=f.read()
# print(f1)
# f.close()

# 读取当前文件
# f = open('a.txt',encoding='utf-8')
# f1=f.read()
# print(f1)
# f.close()
# 相对路径
f = open(r'..\day7\zzz\yyyy\a.txt',encoding='utf-8')
print(f.read())
# f.close()
# 上下文管理:
# with open(...) as f:
#     pass
# # 可以自动关闭文件
# with open(r'a.txt',encoding='utf-8')as f:
#     print(f.read())
















```

### 3.文件操作的常用模式

```
'''
*****
一 文件的打开模式
    r: 只读模式(默认的)
    w: 只写模式
    a: 只追加写模式
二 控制读写文件单位的方式(必须与r\w\a连用)
    t : 文本模式(默认的),一定要指定encoding参数
        优点: 操作系统会将硬盘中二进制数字解码成unicode然后返回
        强调:只针对文本文件有效
    b: 二进制模式,一定不能指定encoding参数
        优点:
'''
#一 rt: 只读模式(默认的)
# 1 当文件不存时,会报错
# 2 当文件存在时,文件指针指向文件的开头

# with open('a.txt',mode='rt',encoding='utf-8')as  f:
#     res1 = f.read()
    # print('1>>>',res1)
    # # # 第一次读完了
    # res2 = f.read()
    # print('2>>>',res2)
    # 判断rt模块可读
    # print(f.readable())
    # # # 判断rt模式不可写
    # print(f.writable())
    # read 文件太大不好
    # print(f.readline(),end='')
    # # #文件里面有换行符 print自带换行符\n
    # print(f.readline())
    # for循环遍历文件对象
    # for line in f:
    #     print(line,end='')
    # L = []
    # for line in f:
    #     L.append(line)
    # print(L)
    # 一行代码搞定
    # print(f.readlines())

# 二 wt: 只写模式
# 1 当文件不存时,新建一个空文档(无则创建)
# with open('b.txt',mode='wt',encoding='utf-8')as  f:
#     pass
# 2 当文件存在时,清空文件内容，文件指针跑到文件的开头（有则清空）
# with open('b.txt',mode='wt',encoding='utf-8')as  f:
#     # 全部清空
#     # 下面写我们想要的内容
#     # 不能读
#     # print(f.readable())
#     # # 可以写
#     # print(f.writable())
#     # f.write(字符串)
#     # f.write('海\n')
#     # f.write('海\n')
#     # f.write('海\n')
#     # f.write('海\n')
#     # 一次性写多行
#     # f.write('111\n2222\n3333\n')
#     # 把列表内容一行行写入
#     info = ['xiao海\n', 'xiao海\n', 'xiao海\n']
#     # for line in info:
#     #     f.write(line)
#     # 一行代码搞定
#     # writelines(列表)
#     f.writelines(info)

# 三 at: 只追加写模式
# 1 当文件不存时,新建一个空文档，文件指针跑到文件的末尾(开头就是末尾)
# with open('c.txt',mode='at',encoding='utf-8')as  f:
#     pass
# 2 当文件存在时,文件指针跑到文件的末尾
# with open('c.txt',mode='at',encoding='utf-8')as  f:
#     # # 不能读
#     # print(f.readable())
#     # # 能写
#     # print(f.writable())
#     f.write('a海\n')
#     f.write('a海\n')
#     f.write('a海\n')
#     f.write('a海\n')
# with open('c.txt',mode='at',encoding='utf-8')as  f:
#     # # 不能读
#     # print(f.readable())
#     # # 能写
#     # print(f.writable())
#     f.write('b海\n')
#     f.write('b海\n')
#     f.write('b海\n')
#     f.write('b海\n')
# w模式和a模式的区别
# wt模式
# 在文件打开不关闭的情况下，连续的写入，
# 下一次写入一定是基于上一次写入指针的位置而继续的
# # a模式关闭了下次打开是在文件末尾写，所以不会覆盖之前的内容
'''
二 控制读写文件单位的方式(必须与r\w\a连用)
    t : 文本模式(默认的),一定要指定encoding参数
        优点: 操作系统会将硬盘中二进制数字解码成unicode然后返回
        强调:只针对文本文件有效

    b: 二进制模式,一定不能指定encoding参数
        优点:
'''
#只能对文本文件操作 t 模式局限性

# 二进制文件 b 模式
# 图片和视频
# with open('1.png',mode='rb') as  f:
#     data=f.read()
#     print(data)
#     print(type(data))
#
# with open('2.png',mode='wb')as f1:
#     f1.write(data)

# 用b模式，也可以对文本文件操作，但是要解码
# decode   二进制解码成字符
# encode   字符编码成二进制
#解码   读的时候转换成字符
# with open('b模式.txt',mode='rb')as f:
#     data = f.read()
#     print(data)
#     print(type(data))
#     print(data.decode('utf-8'))
#编码  写的时候把字符转换成二进制写入
with open('wb模式.txt',mode='wb')as f:
    f.write('dahai\n'.encode('utf-8'))
    f.write('dahai\n'.encode('utf-8'))
    f.write('dahai\n'.encode('utf-8'))




```

### 4.可读可写模式

```
# 可读可写:（了解）
# r+t

# w+t

# a+t

#  r + t
# 1 当文件不存时,会报错
# 2 当文件存在时,文件指针指向文件的开头
# 3 多了个末尾写
# with open('可读可写r+t模式.txt',mode='r+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     msg = f.readline()
#     print(msg)
#     f.write('xxxxxxxxxxx')

# w+t
# 1 当文件不存时,新建一个空文档(无则创建)
# 2 当文件存在时,清空文件内容，文件指针跑到文件的开头（有则清空）
# 3 可以读
# with open('可读可写w+t模式.txt',mode='w+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     f.write('aaaaaaaa\n')
#     f.write('bbbbbbbb\n')
#     # 指针移动seek（移动的字节数,开头开始0）
#     # 从开头开始移动0
#     f.seek(0,0)
#     print(f.readline())
#     #     还是在末尾写
#     f.write('cccccccc\n')

# a+t# 第二次打开时候也是在末尾写
# a 和 w的区别
# with open('可读可写a+t模式.txt',mode='a+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     f.write('aaaaaaaa\n')
#     f.write('bbbbbbbb\n')
#     # 指针移动seek（移动的字节数,开头开始0）
#     # 从开头开始移动0
#     f.seek(0,0)
#     print(f.readline())
#     #     还是在末尾写
#     f.write('cccccccc\n')

# 图片和视频用不上
# r+b w+b a+b 规律和 r+t  w+t   a+t
# 乱掉 文件打不开
```

### 5.指针移动

```
# f.seek *****
# 文件内指针移动,只有t模式下的read(n),n代表的字符的个数
# b模式文件内指针的移动都是以字节为单位


# t模式
# with open('指针移动.txt',mode='rt',encoding='utf-8')as f:
#     print(f.read(1))
#     print(f.read(1))
#     print(f.read(1))
# b模式
# with open('指针移动.txt', mode='rb')as f:
#     #     # 2个16进制是2**4    2**8
#     #     # 三分之一个汉字
#     print(f.read(1))
#     print(f.read(1).decode('utf-8'))
#     print(f.read(3).decode('utf-8'))
# 指针操作
# f.seek(offset,whence)有两个参数:
# offset: 代表控制指针移动的字节数
# whence: 代表参照什么位置进行移动
#        whence = 0: 参照文件开头(默认的),特殊???,可以在t和b模式下使用
#        whence = 1: 参照当前所在的位置,必须在b模式下用
#        whence = 2: 参照文件末尾,必须在b模式下用
# t模式 移动的字节数算 读的按照字符算
# with open('seek.txt',mode='rt',encoding='utf-8')as f:
#     f.seek(2,0)
#     print(f.read(1))

# b模式 移动的字节数 读的也是字节数
# with open('seek.txt',mode='rb')as f:
#     f.seek(2,0)
#     print(f.read(3).decode('utf-8'))
#           whence = 1: 参照当前所在的位置,必须在b模式下用
#        whence = 2: 参照文件末尾,必须在b模式下用
# with open('seek.txt',mode='rb')as f:
#     msg =f.read(5)
#     print(msg.decode('utf-8'))
#     print(f.tell())
#     f.seek(3,1)
#     print(f.read(3).decode('utf-8'))
#        whence = 2: 参照文件末尾,必须在b模式下用
with open('seek.txt',mode='rb')as f:
    # f.seek(0,2)
    # print(f.tell())
    f.seek(-3,2)
    print(f.read(3).decode('utf-8'))






```

### 6.修改文件的方式

```
# *****
# 修改文件的方式一:
# 1 将文件内容由硬盘全部读入内存
# 2 在内存中完成修改
# 3 将内存中修改后的结果覆盖写回硬盘
# with open('文件修改.txt',mode='rt',encoding='utf-8')as f:
#     all_data=f.read()
#     print(all_data)
# # # 读出来的数据已经存到all_data变量里面的了
# with open('文件修改.txt',mode='wt',encoding='utf-8')as f1:
#     f1.write(all_data.replace('红黄蓝','大海'))

# 修改文件的方式二:
# 1 以读的方式打开源文件,以写的方式打开一个临时文件
# 2 从源文件中每读一样内容修改完毕后写入临时文件,直到源文件读取完毕
# 3 删掉源文件,将临时文件重命名为源文件名
# import os
# with open('文件修改二.txt',mode='rt',encoding='utf-8')as read_f\
#     ,open('临时文件.txt',mode='wt',encoding='utf-8')as write_f:
#     for line in read_f:
#         print(line)
#         write_f.write(line.replace('大海','夏洛'))
#
# # 文件修改二删除
# os.remove('文件修改二.txt')
# # # 临时文件.txt 改成 文件修改二
# os.rename('临时文件.txt','文件修改二.txt')


# 方式一:
# 优点: 在文件修改的过程中硬盘上始终一份数据
# 缺点: 占用内存过多,不适用于大文件


# 方式二:
# 优点: 同一时刻在内存中只存在源文件的一行内容,不会过多地占用内存
# 缺点: 在文件修改的过程中会出现源文件与临时文件共存,硬盘上同一时刻会有两份数据,即在修改的过程中会过多的占用硬盘,

```

### 7.如何避免乱码

```
# 天生我才必有用
# 日语
with open('text1.txt',mode='w',encoding='shift_jis')as f1:
    f1.write('生まれながらにしてわたくし私はかならず必ずやく役にたつ立つ')

with open('text1.txt',mode='r',encoding='shift_jis')as f1:
    a=f1.read()
    print(a)

# ！！！总结非常重要的两点！！！
#1、保证不乱码的核心法则就是，字符按照什么标准而编码的，
# 就要按照什么标准解码，此处的标准指的就是字符编码
#2、在内存中写的所有字符，一视同仁，都是unicode编码，比如我们打开编辑器，
# 输入一个“你”，我们并不能说“你”就是一个汉字，此时它仅仅只是一个符号，
# 该符号可能很多国家都在使用，根据我们使用的输入法不同这个字的样式可能也不太一样。
# 只有在我们往硬盘保存或者基于网络传输时，
# 才能确定”你“到底是一个汉字，还是一个日本字，这就是unicode转换成其他编码格式的过程了
```

