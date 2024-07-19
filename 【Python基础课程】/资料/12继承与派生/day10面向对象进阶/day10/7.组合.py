'''
1. 什么是组合 ****
    组合指的是某一个对象拥有一个属性,该属性的值是另外一个类的对象
'''
# class Foo:
#     xxx = 100
# class Bar:
#     yyy = 200
#     def zzz(self):
#         print('我是Bar类实例化对象的方法')
# obj=Foo()
# obj1=Bar()
#
# obj.attr = obj1
# print(obj.xxx)
# # obj.attr 等价于 obj1
# print(obj.attr)
# print(obj1.yyy)
# print(obj.attr.yyy)
# obj1.zzz()
# obj.attr.zzz()
'''
2. 为何要用组合
    通过为某一个对象添加属性(属性的值是另外一个类的对象)的方式,可以间接地将两个类关联/整合/组合到一起
    从而减少类与类之间代码冗余
'''
# class Foo1:
#     pass
# class Foo2:
#     pass
# class Foo3:
#     pass
# class Bar:
#     pass
# obj_from_bar = Bar()
# obj1 = Foo1()
# obj2 = Foo2()
# obj3 = Foo3()
# # # 我可以把这些对象都添加Bar对象作为组合
# obj1.attr1 = obj_from_bar
# obj2.attr2 = obj_from_bar
# obj3.attr3 = obj_from_bar
'''
3. 如何用组合
'''
class People:
    HP = 100
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
class Teacher(People):
    def __init__(self,name,age,sex,course = []):
        super().__init__(name,age,sex)
        self.course = course
    def tell_info1(self):
        # print(self.course)
        for i in self.course:
            # print(i) # 课程对象
            # 通过课程对象拿到课程属性
            # print('<课程名:%s 价钱:%s>' % (i.c_name, i.c_price))
            # 课程方法
            i.tell_info()
class Student(People):
    def __init__(self,name,age,sex):
        People.__init__(self,name,age,sex)
class Course:
    def __init__(self, c_name, c_price):
        self.c_name = c_name
        self.c_price = c_price
    def tell_info(self):
        print('<课程名:%s 价钱:%s>' % (self.c_name, self.c_price))
python=Course('python开发',10000)
math = Course('高等数学',3000)
English = Course('英语',2000)
music = Course('音乐',4000)
drawing = Course('绘画',4000)
# python.tell_info()
tea = Teacher('大海',26,'man')
# 把music课程对象添加到老师对象tea的属性里面
# tea.course = music
# # # tea.course它是一个对象music
# # # 在添加一个就替换了成drawing，这样不行
# tea.course = drawing
# tea.course.tell_info()

# 如果我想把一堆的对象放到一个对象属性里面，我们怎么做？
# 思考一下？列表
# 把对象的属性定义成列表，写一个默认参数
print(tea.course)
tea.course.append(music)
tea.course.append(English)
tea.course.append(math)
print(tea.course)

# tea.course.tell_info()
print(tea)
print('===========')
tea.tell_info1()

'''
4.组合和继承的区别，继承是把全部的属性和方法让子类可以调用，
而组合只是部分的属性和方法把2个类关联到一起，有些类的属性
不能全部继承，这就用到了组合,组合的是对象，而继承的是类
继承是在类定义产生的，它是类之间的关联关系，
而组合是类定义后产生的关系，因为
它是对象的关联关系
'''




























