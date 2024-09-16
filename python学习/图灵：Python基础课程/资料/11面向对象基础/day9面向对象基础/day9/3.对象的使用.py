
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
        # print(self)
        print('course')
        return 'aaaaa'
    # print('类的定义我运行了')
#2. 后调用类来产生对象:
# 调用类的过程称之为类的实例的初始化,调用类的返回值称之为类的一个对象/实例
# 调用类发生了?
# 类是抽象  对象/实例是具象

# 产生3个老师对象
t1=Teacher()
t2=Teacher()
t3=Teacher()

# print(t1)
# 生成的对象拥有类的属性和方法
print(t1.name)
print(t2.name)
print(t3.name)

# 对象的方法
# print(t1.course)
# print(t2.course)
# print(t3.course)

## 这些对象没有独立的属性，用的是类的属性和方法
# print(Teacher.__dict__)
# print('===========')
# print(t1.__dict__)
# print(t2.__dict__)
# print(t3.__dict__)

# ?????
#对象的方法执行，没有传入参数，self到达是什么？
# a=t1.course()
# print(a)

# 对比类方法执行,需要传入参数
# Teacher.course(222)

# 一样有return
# print('=====')
# print(Teacher.course(111))
# print(t1.course())

# 对象属性的修改
# print(t1.__dict__)
t1.name = '夏洛'
# # # 对象没有name属性，用类的属性
# print(t1.name)
# # 这个属性是对象独立的
# print(t1.__dict__)
#
# # 删除对象的属性
# # 删除的是   t1.name = '夏洛'
# del t1.name
#
# print(t1.name)



