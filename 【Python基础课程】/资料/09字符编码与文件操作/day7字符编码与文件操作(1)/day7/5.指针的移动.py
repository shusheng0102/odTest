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





