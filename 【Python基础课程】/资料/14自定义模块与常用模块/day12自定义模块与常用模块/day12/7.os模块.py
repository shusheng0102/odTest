"""
    OS模块 *****
        os表示操作系统相关
        os模块是与操作系统交互的一个接口
        就是围绕文件和目录的操作
"""
# 工作目录，当前目录，父级目录都是一个day12
import os
# 获取当前工作目录，绝对路径
# print(os.getcwd())
# 生成目录
# os.mkdir('dirname1')
# 空目录，若目录不为空则无法删除
# os.rmdir('dirname1')

# os.mkdir('dirname')
# os.rmdir('dirname')
# # 拿到当前脚本工作的目录，相当于cd
# os.chdir('dirname')
# # 删除文件
# os.remove('aaaa.py')
# os.rmdir('dirname')
# 可生成多层递归目录
# os.makedirs('dir1/dir2/dir3/dir4')
# 在dir2下面创建一个文件，会产生保护机制只删除到dir2
# os.removedirs('dir1/dir2/dir3/dir4')

# 拿到当前文件夹的文件名或者文件夹放入列表
# 绝对路径
# print(os.listdir(r'D:\python代码2\day12'))
# 相对路径
# print(os.listdir('.'))
# 上一级
# print(os.listdir('..'))
# 重命名文件/目录
# os.rename('oldname','newname')

# 运行终端命令
# os.system('tasklist')
# python D:\python代码2\day12\7.os模块.py

# os.path 下面的方法  path是路径
# 将path分割成目录和文件名二元组返回
print(os.path.split('/a/b/c/d.txt'))
# 文件夹
# print(os.path.split('/a/b/c/d.txt')[0])
# # 文件
# print(os.path.split('/a/b/c/d.txt')[1])
#返回path的目录。其实就是os.path.split(path)的第一个元素
print(os.path.dirname('/a/b/c/d.txt'))
# 返回path最后的文件名。即os.path.split(path)的第二个元素
print(os.path.basename('/a/b/c/d.txt'))
# 判断路径是否存在 文件和文件夹都可以 如果path存在，返回True；如果path不存在，返回False
print(os.path.exists('D:\python代码2\day12'))
print(os.path.exists('D:\python代码2\d12'))
print(os.path.exists(r'D:\python代码2\day12\4.hash模块.py'))
# 如果path是一个存在的文件，返回True。否则返回False
print(os.path.isfile(r'D:\python代码2\day12\4.hash模块.py'))
# 也可以用相对路径
print(os.path.exists(r'./4.hash模块.py'))
print(os.path.exists(r'../day12/4.hash模块.py'))
# 如果path是一个存在的目录，则返回True。否则返回False
print(os.path.isdir('D:\python代码2\day12'))
print(os.path.isdir('D:\python代码2\da2'))
# 拼接一个绝对路径，会忽略前面的路径
print(os.path.join('a','b','c','D:\\','f','d.txt'))
print(os.path.join('D:\\','f','d.txt'))










