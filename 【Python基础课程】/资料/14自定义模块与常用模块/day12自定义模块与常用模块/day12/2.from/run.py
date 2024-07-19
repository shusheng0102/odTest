# 首次导入模块发生3件事
# 1. 创建一个模块的名称空间
# 2. 执行文件spam.py,将执行过程中产生的名字都放到模块的名称空间中
# 3. 在当前执行文件中直接拿到一个名字,该名字就是执行模块中相对应的名字的
# from 模块名  import 各种名字变量名，函数名等等
# money = 100
# from spam import money,read1
#
# print(money)
# read1()

# *代表从被导入模块中拿到所有名字（不推荐使用）
# from spam import *
# print(money)
# read1()
# print(A)

# 起别名
# from spam import money as r1
# print(r1)

# 总结from...import...
# 优点: 使用时,无需再加前缀,更简洁
# 缺点: 容易与当前名称空间中的名字冲突

# from 文件夹 import 模块名
# 绝对导入
# from dir import m1
# from dir.m1 import f1
#
# f1()
# m1.f1()
# m1.f2()
# m1.f3()




