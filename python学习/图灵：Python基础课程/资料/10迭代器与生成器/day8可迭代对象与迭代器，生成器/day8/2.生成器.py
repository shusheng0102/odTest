#大前提：生成器就是一种自定义的迭代器，本质就是迭代器
# 但凡函数内包含yield关键字，调用函数不会执行函数体代码，
# 会得到一个返回值，该返回值就是生成器对象
# def func():
#     print('=====1')
#     yield 1
#     print('=====2')
#     yield 2
#     print('=====3')
#     yield 3
# g=func()
# # print(g)
# # print(g is g.__iter__().__iter__())
# # g.__next__()
# res1=next(g)
# # #  #会触发函数的执行，直到碰到一个yield停下来，并且将yield后的值当作本次next的结果返回
# print(res1)
# res2=next(g)
# print(res2)
# res3 = next(g)
# print(res3)
# 报错和迭代器一样,代表取完了
# next(g)
# for i in g:
#     print(i)
# 总结yield:只能在函数内使用
#1. yield提供了一种自定义迭代器的解决方案
#2. yield可以保存函数的暂停的状态
#3. yield对比return
#   1. 相同点：都可以返回值，值的类型与个数都没有限制
#   2. 不同点：yield可以返回多次值，而return只能返回一次值函数就结束了
# '''
# 定义一个生成器，这个生成器可以生成10位斐波拉契数列，得到斐波拉契数列
# # （斐波那契数列：数列中每一个数的值都等于前两个数相加的值 [1, 1, 2, 3, 5, 8, 13, 21, 34, 55.........]）
# '''
# # i是计算循环的  a第一个数  b第二个数
# def run(n):
# # # n 代表数列的个数
#     i ,a ,b = 0, 1,1
#     while i < n:
#         yield a # a 第一次是a 1  b 1  第二次 a 1  b 2  第三次 a 2  b 3  第四次 a 3 b 5  第五次 a 5 b 8
#         a ,b = b ,a + b
#         i +=1
# my_run=run(10)
# print(my_run)
# # print(list(my_run))
# print('=========1')
# for i in my_run:
#     print(i)
# print('=========2')
# for i in my_run:
#     print(i)

# 了解
# 千与千寻
# 函数可不可以不断传值
# yield的表达式形式的应用: x=yield
# 不停的传值

# def run1(name):
#     print('千与千寻%s准备开吃'%name)
#     food_list = []
#     while True:
#         food=yield  food_list
#         print('%s吃了%s'%(name,food))
#         food_list.append(food)
#
# g=run1('无脸男')
# # print(g)
# res1=next(g)
# print(res1)
# # # 1. 先为当前暂停位置的yield赋值 2. next(生成器)直到再次碰到一个yield停下来，
# res2=g.send('青蛙')
# print(res2)
# res3=g.send('黄金')
# print(res3)
# res3=g.send('黄金')
# print(res3)
# res3=g.send('黄金')
# print(res3)






















