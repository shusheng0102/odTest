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



