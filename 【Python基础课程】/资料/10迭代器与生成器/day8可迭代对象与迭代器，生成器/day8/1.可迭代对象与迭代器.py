'''
1. 什么是迭代器
    迭代就是更新换代
    1.1. 迭代器指的是迭代取值的工具
    1.2. 迭代是一重复的过程，每一次重复都是基于上一次的结果而来
    比如：爹生了儿子，儿子生了孙子
    编程来源生活 ：有些事情不用一次性追求完美
        1.第一次开发的项目，互联网公司
        前面实现基本功能，保证用户量
        后面可以慢慢改，提升品质
        2.老师第一次上课，紧张，技术难点，第一次不可能
        讲的完美，但是慢慢提升，也是一个迭代的过程
        3.同学们有一个知识点没懂，比如装饰器
        完美没必要放弃，掌握@+装饰器名字就ok
        学习也是一个迭代的过程，它是基于上次学习的结果的
        一次理解了60%，下次看看变成80%，运用了100%。
        4.第一次恋爱，也不可能完美，也是慢慢提升的过程
2. 为何要用迭代器
    器是工具
    迭代器提供了一种通用的且不依赖于索引的迭代取值方式的功能
3. 如何用迭代器

'''
#单纯的重复不是迭代
# i = 0
# while True:
#     print(i)
# 迭代：重复+每次重复都是基于上一次的结果而进行（不是是单纯的重复）
# L = ['a','b','c']
# i = 0
# while i<len(L):
#     print(L[i])
#     i += 1
# # 哪些数据类型需要这样迭代取值
# # 字符串 列表 元组 字典 集合 文件等等
# L = ['a','b','c']
# L = 'abc'
# L = ('a','b','c')
# i = 0
# while i<len(L):
#     print(L[i])
#     i += 1
# 所以我们需要一种不依赖索引取值的方式
# 迭代器提供了一种通用的且不依赖于索引的迭代取值方式的功能

# 可迭代对象
#一 ：可迭代的对象iterable：但凡内置有__iter__方法的对象都称之为可迭代的对象
# 作者是个天才，每个需要取值的都加了__iter__方法
#可迭代的对象：str，list，tuple，dict，set,文件对象
# a = 1
# # # a.__iter__没有
# b = 1.1
# # # b.__iter__没有
# c= 'hello'
# # # c.__iter__()
# d= ['a','c']
# # # d.__iter__()
# e = {'x':1}
# # # e.__iter__()
# g ={1,2,3}
# # g.__iter__()
# f = open('b.txt','rt',encoding='utf-8')
# # # f.__iter__()
# print(f.__next__())
# print(f.__next__())


# 迭代器
# 执行可迭代对象下的__iter__方法，返回的值就是一个迭代器对象

# dic = {'x':1,'y':2,'z':3}
# # 可迭代对象变成迭代器
# iter_dic=dic.__iter__()
# print(iter_dic)
# 迭代器的__next__()可以迭代取值
# print(iter_dic.__next__())
# print(iter_dic.__next__())
# print(iter_dic.__next__())
# # #StopIteration应该被当成一种结束信号，代表迭代器取干净了
# print(iter_dic.__next__())
# 列表不依赖索引取值
# l = [1,2,3]
# iter_l=l.__iter__()
# print(iter_l)
# print(iter_l.__next__())
# print(iter_l.__next__())
# print(iter_l.__next__())
# # # #StopIteration应该被当成一种结束信号，代表迭代器取干净了
# print(iter_l.__next__())

# 误区
# l = [1, 2, 3]
# print(l.__iter__().__next__())
# # # 基于新的迭代器对象
# print(l.__iter__().__next__())
# 迭代是基于老的
# iter_l=l.__iter__()
# print(iter_l.__next__())
# print(iter_l.__next__())
# print(iter_l.__next__())

# 可迭代对象与迭代器
# 可迭代对象
# 只有__iter__方法，没有__next__方法
# 除了文件其他容器都是可迭代对象
# 迭代器
#1. 既内置有__next__方法的对象，执行迭代器__next__方法可以不依赖索引取值
#2. 又内置有__iter__方法的对象，执行迭代器__iter__方法得到的仍然是迭代器本身
# 1 迭代器一定是可迭代的对象，而可迭代的对象却不一定是迭代器
#    可迭代的对象只需要有__iter__()
#    迭代器对象 __iter__()  __next__()
# 2.文件对象本身就是一个迭代器
# f = open('b.txt','rt',encoding='utf-8')
# # # f.__iter__()
# print(f.__next__())
# print(f.__next__())

# l = [1,2,3]
# iter_l = l.__iter__()
# #  调用可迭代的对象__iter__得到的是迭代器，
# print(iter_l is iter_l.__iter__().__iter__().__iter__().__iter__())
# # 执行迭代器__iter__方法得到的仍然是迭代器本身,那么有什么用
# # 为了for循环

# #   iter()   next()
# dic = {'x':1,'y':2,'z':3}
# iter_dic = iter(dic)
# print(iter_dic)
# # #底层 print(dic.__iter__())
# print(next(iter_dic))
# # #底层 print(iter_dic.__next__())


# 解决迭代器报错
# 异常捕获
# while True:
#     try:
#         print(next(iter_dic))
#     except StopIteration:
#         break
# print('===============')
# # # # 同一个迭代器只能完整地取完一次值
# while True:
#     try:
#         print(next(iter_dic))
#     except StopIteration:
#         break

# 有没有一种好的方法自己把
# 1.可迭代对象变成迭代器
# 2.能够自己获取迭代器对象next的值
# 3.next最后不报错
#for本质应该称之为迭代器循环  *****
# 那么以后大家知道for循环后面可以跟迭代器和可迭代对象
#底层工作原理
#1. 先调用in后面那个对象的__iter__方法，将其变成一个迭代器
    # 如果是个迭代器__iter__可以变成迭代器
    # 如果是个可迭代对象__iter__可以变成迭代器
#2. 调用next(迭代器)，将得到的返回值赋值给变量名  k
#3. 循环往复直到next(迭代器)抛出异常，for会自动捕捉异常StopIteration然后结束循环
# dic = {'x':1,'y':2,'z':3}
# for k in dic:
#     print(k)
# # # 为什么下一次又可以
# # # 因为又做了上面三件事 又变成了一个新的dic迭代器
# for k in dic:
#     print(k)
#迭代器总结
# 优点：
#     1. 提供一种通用的且不依赖于索引的迭代取值方式
#     2. 同一时刻在内存中只存在一个值，更节省内存

# 缺点：
#     1. 取值不如按照索引的方式灵活，（不能取指定的某一个值，而且只能往后取）
#     2. 无法预测迭代器的长度
# 还记得range吗
# obj_iter=range(1,10)
# # # obj_iter可迭代对象
# # print(obj_iter)
# obj_next=iter(obj_iter)
# # obj_next迭代器
# print(obj_next.__next__())
# print(obj_next.__next__())
# print(obj_next.__next__())
# print('迭代器的for循环')
# for i in obj_next:
#     print(i)
# print('aaaaaaaaaa')
# for i in obj_next:
#     print('dahai%s'%i)
# print('可迭代对象for循环1')
# for i in obj_iter:
#     print(i)
# print('可迭代对象for循环2')
# for i in obj_iter:
#     print(i)




# 了解
# lst = [1, 2, 3]
# from collections import Iterable  # 可迭代对象
# from collections import Iterator  # 迭代器
#
# print(isinstance(lst,list))
# print(isinstance(lst,Iterable))# 可迭代对象
# print(isinstance(lst.__iter__(),Iterator))# 迭代器



