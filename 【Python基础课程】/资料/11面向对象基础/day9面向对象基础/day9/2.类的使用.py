'''
类
老师
属性
    name='大海'
    age=18
    sex='男'
技能/方法
    上课
# class 定义类的关键字    类名首字母大写（约定俗成的）
class 类名:
    pass
复杂的类名和变量一样
# 驼峰体
AgeOfDahai = 18
定义示例：
class Person:
    pass

'''
#1. 先定义类
class Teacher:
    # 相同的特征/属性/变量
    name = '大海'
    age = 18
    sex = '男'
    # 函数/方法/技能
    def course(self):
        # self到底是什么？
        # self当做一个位置形参
        print(self)
        print('course')
    # print('类的定义我运行了')
#类是一系列对象相同的属性(变量)与技能(函数)的结合体,
# 即类体中最常见的就是变量与函数的定义
# 类体代码会在类定义阶段立即执行,会产生一个类的名称空间,
# print(Teacher.__dict__)
# 调用类的属性
# print(Teacher.name)
# print(Teacher.age)
# print(Teacher.sex)

# 类的方法其实就是函数
# print(Teacher.course)

# 函数加括号调用
# ？？？？？
# self我们现在把它当作一个位置形参，但是为什么定义成self呢？
# Teacher.course(111)

# # 不存在的属型或者方法会报错
# print(Teacher.xxx)

# 修改类属性的值
# Teacher.name = '夏洛'
#
# print(Teacher.name)

# 添加类的属性
# Teacher.play = '篮球'
# # print(Teacher.play)
# print(Teacher.__dict__)
#
# del Teacher.play
# print(Teacher.__dict__)

# 总结:
# 1. 类本质是一个用来存放变量与函数的容器
# 2. 类的用途之一就是当做容器从其内部取出名字来使用
# 3. 类的用途之二是调用类来产生对象 接下来讲对象



