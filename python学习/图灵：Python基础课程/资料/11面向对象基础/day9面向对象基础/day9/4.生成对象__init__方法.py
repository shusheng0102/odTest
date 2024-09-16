'''
### 1、初始化 *****
以双下划线开头且以双下划线结尾的固定方法，他们会在特定的时机被触发执行，
__init__就是其中之一，它会在实例化之后自动被调用，以完成实例的初始化。
'''
#1. 先定义类
class Teacher:
    # 相同的特征/属性/变量
    school = 'tuling'
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    # 函数/方法/技能
    def course(self,name):
        # self到底是什么？
        # self当做一个位置形参
        # print(self)
        print('%s上课'%name)
        # return 'aaaaa'
    # print('类的定义我运行了')
dahai=Teacher('大海',18,'男')
xialuo=Teacher('夏洛',20,'男')
# print(dahai)
# print(xialuo)

# print(dahai.name)
# print(dahai.__dict__)
# print(xialuo.name)
# # __init__方法传入的属性类是没有的
# # print(Teacher.name)
#
# # 只是初始化的时候传入了参数，对象还是可以改属性值
# dahai.name = '顾安'
# print(dahai.name)

# 对象方法传入参数有其他参数
dahai.course('dahai')



