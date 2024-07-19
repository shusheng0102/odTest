# 装饰器就是一个特殊的闭包函数
# 1、什么是装饰器（就是一个函数，只不过这个函数不是给自己使用的，是给其他函数添加功能的）
#     器指的是工具，而程序中的函数就具备某一功能的工具
#     装饰指的是为被装饰器对象添加额外功能
# 2、为什么要用装饰器
#     软件的维护应该遵循开放封闭原则
#     开放封闭原则指的是：
#         软件一旦上线运行后对修改源代码是封闭的，对扩展功能的是开放的
#         这就用到了装饰器
#     装饰器的实现必须遵循两大原则：
#         1、不修改被装饰对象的源代码(人的原来的性格，生活方式)
#         2、不修改被装饰对象的调用方式(人的原来的外貌，名字)
# def run():
#     print('跑步')
#     print('健身')
# run()
# def fitness():
#     print('健身')
#     run()
# def run():
#     print('跑步')
# fitness()
# run()
#     装饰器其实就在遵循1和2原则的前提下为被装饰对象添加新功能
# 比如男孩1给女朋友买衣服，项链或化妆品  ， 变的更加自信，原来的外貌，原来的性格没有发生改变 # 装饰器

# 比如男孩2带女朋友去整容   ， 变的更加自信(不一定)， 原来的外貌，原来的性格发生改变 # 不是装饰器

# name = '大海'
# def run(name):
#     print('=========')
#     print('我是%s'%name)
#     print('=========')
# # run(name)
#
# def decorate(func): # func等下我们要传入的run
#     def new_func(name):#  run(name) 的name
#         print('我是装饰函数前面的代码')
#         func(name)#  run(name)
#         print('我是装饰函数后面的代码')
#     return new_func
# # 一 1.定义了new_func(name)函数 ，2.返回 了new_func内存地址 3.传入了一个run函数名
# run=decorate(run)
#
#
# # print(a)
# run(name)
# # 测试for循环从1加到9000000的时间
n = 9000000

from datetime import datetime
def run_time(func):# func 是for1  这是一个用来计算程序执行时间的装饰器
    def new_func(*args,**kwargs):
        start_time = datetime.now()
        print('开始时间%s'%start_time)
        func(*args,**kwargs)#  for1(9000000)
        end_time=datetime.now()
        print('结束时间%s'%end_time)
        time1 = end_time-start_time
        print('花费时间%s'%time1)
    return new_func
# 一 1.定义了new_func(n)函数 ，2.返回 了new_func内存地址 3.传入了一个for1函数名
@run_time # for1=run_time(for1)
def for1(n):
    sum1 = 0
    for i in range(1,n+1):
        sum1 += i
    print(sum1)

@run_time # shopping=run_time(shopping)
def shopping():
    for i in range(1111111):
        pass
    print('我是shopping')
# for1(n)
shopping()
# 换了个马甲for1
# 装饰器的要求高于闭包
#         1、不修改被装饰对象的源代码(人的原来的性格，生活方式)
#         2、不修改被装饰对象的调用方式(人的原来的外貌，名字)




