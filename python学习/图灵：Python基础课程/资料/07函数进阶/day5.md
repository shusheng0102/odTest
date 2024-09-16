## day5

### 1.匿名函数

```
'''
1 匿名函数：就是没有名字的函数

2 为何要用：
    用于仅仅临时使用一次的场景，没有重复使用的需求
'''
# 有名函数
# 断点
# F9 绿色的三角形是调到下一个断点
# F8蓝色朝下的箭头是单步走
# Alt + F9 移动到光标处
# F7蓝色朝右下角的箭头是进入函数
# Alt +shift+F7蓝色朝右下角的箭头是进入函数自己定义的函数
# shif + F8跳出函数
# def sum1(x,y):
# #     print(x,y)
# #     print(x,y)
# #     print(x,y)
# #     return x+y
# # print('11111')
# # sum1(1,2)
# # print('22222')
# # 匿名函数，除了没有名字其他的都有
# # 语法 lambda空格+参数+冒号+函数体代码(表达式或者函数)
# # 一行代码图省事
# # 匿名函数的定义
# print(lambda x,y:x+y)
# # 调用直接内存地址加括号（它虽然没有名字）+括号可以调用
# 返回值省去了return
# 表达式
# print((lambda x,y:x+y)(1,2))
# # 函数
# print((lambda x,y:print(x+y))(1,2))


# # 把内存地址赋值给一个变量没有意义
# # 匿名函数的精髓就是没有名字，为其绑定名字是没有意义的
# f=lambda x,y:x+y
# print(f(1, 2))
# 匿名函数与内置函数结合使用
# max,min,sorted
salaries = {
    'xialuo':3000000,
    'xishi':10000,
    'dahai':3000
}
# # 求薪资最高的那个人名：即比较的是value，但取结果是key
# # 默认比较key值
# print(max(salaries))
# # max(字典,key=函数名)
# def func(name):
#     return salaries[name]
# print(max(salaries, key=func))
# # 在外面我们不要用它
# # func(1)
# # 求最大值即比较的是value工资，但取结果是key人名
# print(max(salaries, key=lambda name: salaries[name]))
#
# # 求最小值
# print(min(salaries, key=lambda name:salaries[name]))
# sorted排序

nums = [11,33,22,9,1]
res = sorted(nums,reverse=True)
print(res)

# 循环遍历薪资
for v in salaries.values():
    print(v)

print(sorted(salaries.values()))
# 但是我们是要比较薪资，返回的却是人名
# 薪资反序
print(sorted(salaries, key=lambda name: salaries[name], reverse=True))
# 薪资正序
print(sorted(salaries, key=lambda name: salaries[name], reverse=False))
```

### 2.递归函数

```
'''
1 什么是递归函数
函数的递归调用是函数嵌套调用的一种特殊形式,在调用一个函数的过程中又直接或者间接地调用该函数
本身,称之为函数的递归调用
递归死循环是没有意义的
递归调用必须有两个明确的阶段:
        1. 回溯: 一次次递归调用下去,说白了就一个重复的过程,
        但需要注意的是每一次重复问题的规模都应该有所减少,
        直到逼近一个最终的结果,即回溯阶段一定要有一个明确的结束条件
        2. 递推: 往回一层一层推算出结果
'''
# 直接调用自己
# def foo(n):
#     print('from foo',n)
#     foo(n+1)
#
# foo(0)

# 第五个人年龄为第4个人加2岁
'''
age(5)=age(4)+2
age(4)=age(3)+2
age(3)=age(2)+2
age(2)=age(1)+2
age(1)=18
'''
# 第几个人定义成n
'''
age(n)=age(n-1)+2 # n > 1
age(n) = 18       # n = 1
'''
# 递归调用就是一个重复的过程,但是每一次重复问题的规模都应该有所减少,
# 并且应该在满足某种条件的情况下结束重复,开始进入递推阶段
# def age(n):
#     # 所以要在这里写递归结束条件
#     #     # 在这个找到条件并且导致函数不再自己调用自己的时候
#     #     # 叫做回溯
#     #     # 从结束条件一步步进行返回的结果
#     #     # 叫做递推
#     if n == 1:
#         return 18
#     # 第一次 # age(5)=age(4)+2                 26
#     #     # 第二次   age(4)=age(3)+2                 24
#     #     # 第三次 # age(3)=age(2)+2                 22
#     #     # 第四次 # age(2)=age(1)+2                 20
#     #     # 但是我们不知道age(1)是多少
#     #     # 第五次 age(1)=18                   递推  18
#     return age(n-1)+2
#
# print(age(5))
L = [1,[2,[3,100,[4,[5,[6,[7,]]]]]]]
# 循环需要考虑次数
# for n in L:
#     # print(n)
#     if type(n) is not list:
#         print('我是数字%s'%n)
#     else:
#         # 以下是重复的过程
#         for i in n:
#             print(i)
#         else:
#             pass

# def search(L):
#     for n in L:
#         # print(n)
#         if type(n) is not list:
#             print('我是数字%s'%n)
#         else:
#             # print(n)
#             search(n)
# search(L)
# 递归与循环的区别，循环每一次都要判断，需要考虑多少次
# 而递归只需要确定结束条件就行，按照规律进行重复调用，不需要考虑次数









```

### 3.闭包函数

```
# 闭包函数
# 闭包
# 闭指的是:该函数是一个内部函数
# 包指的是:指的是该内部的函数名字在外部被引用
# # # 1、函数定义阶段:
# # # 只检测函数体的语法( 工厂合不合格)，不执行函数体代码 （不使用工厂）
# def factory():#  制造一个工厂
#     print('正在制造手机')# 代码相对于员工或者机器
# # # 2、函数调用阶段:
# # # 1 先找到名字   (找到工厂的位置)
# # # # 2 根据名字调用代码   ( 加了括号执行工厂进行加工)
# #
# factory()

# 闭包
# 闭指的是:该函数是一个内部函数
# 包指的是:指的是该内部的函数名字在外部被引用
# def outer():# 没有调用outer(),但是创造了outer这个函数
#     # 1 只检测函数体outer的语法( 工厂合不合格)，不执行函数体代码 （不使用工厂）
#     print('外面的函数正在运行')
#     def inner():
#         print('里面的函数正在运行')
#     return inner# 3返回inner函数的内存地址  想象成一个钥匙 控制里面工厂
#
# # 创造了inner这个函数
# # print(outer())
# # # 4 得到里面工厂的钥匙 钥匙取一个名字innera
# #
# inner=outer() #2 定义了inner函数
# # print(inner)
# # # 5 里面钥匙加括号就可以开启里面的工厂
# inner()

# 为函数体传值的方式一：参数
# def func(x,y):
#     print(x+y)
# func(1,2)
# func(1,2)
# func(1,2)
# func(1,2)
# 为函数体传值的方式二：闭包
# def outer(x,y):
#     def func():
#         print(x + y)
#     return func
#
# func=outer(1,2)
# func()
# func()
# func()
# func()







```

### 4.装饰器

```
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





```
### 有名函数

```
# 断点
# 打断点
# 启动断点 鼠标右键
# ctrl + F5 重启程序
# ctrl + F2 停止
# F9 绿色的三角形是调到下一个断点
# F8 蓝色朝下的箭头是单步走
# Alt + F9 移动到光标处
# Alt +shift+F7蓝色朝右下角的箭头是进入函数自己定义的函数
# F7蓝色朝右下角的箭头是进入函数
# shif + F8跳出函数

def sum1(x,y):
    print(x)

    print(y)

    print(x,y)

    return x+y
print('11111')
sum1(1,2)
print('222222')
```

### 作业

```
'''
1.上课的内容敲5遍，解释一下各个函数的作用。
2.写一个登录装饰器对以下函数进行装饰，要求输入账号和密码才能运行该函数
def run():
    print('开始执行函数')
'''
```