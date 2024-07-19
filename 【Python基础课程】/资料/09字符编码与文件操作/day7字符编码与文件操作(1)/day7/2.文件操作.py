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















