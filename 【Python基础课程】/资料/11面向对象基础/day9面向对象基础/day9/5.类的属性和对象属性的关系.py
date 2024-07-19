# *****
#1. 先定义类
class Teacher:
    # 相同的特征/属性/变量
    school = 'tuling'
    xxx = '我是类的属性,也可能是对象的属性'
    yyy = 111
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    # 函数/方法/技能
    def course(self):
        # self到底是什么？
        # self当做一个位置形参
        # print(self)
        print('%s上课'%self.name)
dahai=Teacher('大海',18,'男')
xialuo=Teacher('夏洛',20,'男')
guan=Teacher('顾安',20,'男')

# 对象属性的查找
# 添加一个对象属性
# dahai.xxx = '我是对象的属性'
# 属性查找优先找对象，对象没有才去类里面找
# print(dahai.xxx)

# 类中定义的属性和方法是所有对象共享的,类可以用，对象也可以用
# 类的属性给对象调用
# print(id(dahai.yyy),dahai.yyy)
# print(id(xialuo.yyy),xialuo.yyy)
# print(id(guan.yyy),guan.yyy)
# # 类自己用
# print(id(Teacher.yyy),Teacher.yyy)

# 类的属性变化
# Teacher.yyy = 33333
# dahai.yyy =22222
# # 类的属性给对象调用
# # 对象已经有了yyy属性的会优先考虑自己的
# print(id(dahai.yyy),dahai.yyy)
# # 其他没有对象yyy属性的都会跟随类yyy属性的改变而改变
# print(id(xialuo.yyy),xialuo.yyy)
# print(id(guan.yyy),guan.yyy)
# # 类自己用
# print(id(Teacher.yyy),Teacher.yyy)

# ？？？？？？
# 对象调用类的方法,不需要传入参数？
# print(id(dahai.course))
# dahai.course()
#
# print(id(xialuo.course))
# xialuo.course()
#
# print(id(guan.course))
# guan.course()

# 类调用方法必须传入self参数对应的对象,因为方法里面需要使用这个self对象
# Teacher.course(dahai)
# Teacher.course(guan)
# Teacher.course(xialuo)


