## day10继承与派生

### 1.继承介绍

```
'''
1 什么是继承
    继承一种新建类的方式,新建的类称之为子类/派生类,被继承的类称之为父类\基类\超类
    python中继承的特点:
        1. 子类可以遗传/重用父类的属性 或者方法
2 为何要用继承
    减少类与类之间代码冗余
3 如何用继承 *****
# 子类
class Parent(父类):
    pass
'''

# class Parent():
#     xxx = 333
#     def run(self):
#         print('我是父类的方法')
# class Sub(Parent):
#     # xxx = 222
#     pass
# obj=Sub()
#
# # obj.xxx = 111
# # ,属性查找的优先级
# # 优先调用对象属性,
# # 子类有属性就用子类的,没有就访问父类的
# print(obj.xxx)
# obj.run()













```

### 2.利用继承来解决类与类之间代码冗余问题

```
'''
总结对象的相似之处得到了类 *****
总结类的相似之处得到父类 *****
'''
class People:
    sclool = '图灵学院'
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex
class Student(People):
    # def __init__(self,name,age,sex):
    #     self.name=name
    #     self.age=age
    #     self.sex=sex
    def play(self):
        print('%s play football'%self.name)
class Teacher(People):
    # def __init__(self,name,age,sex):
    #     self.name=name
    #     self.age=age
    #     self.sex=sex
    def course(self):
        print('%s course'%self.name)

s1 = Student('周阳',38,'male')
print(s1.__dict__)
t1 = Teacher('大海',18,'man')
print(t1.__dict__)

#1 但是这里有个问题子类有新的属性需要实例化的时候参数怎么办?











```

### 3 在子类派生的新方法中重用父类功能的方式一

```
'''
# 子类重用父类的功能 *****
# 在子类派生出的新方法中重用父类功能的方式一:
# 指名道姓地引用某一个类中的函数
# 总结:
# 1. 与继承无关
# 2. 访问是类的函数,没有自动传值的效果
'''
class People:
    sclool = '图灵学院'
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex
# s1 = People('周阳',38,'male')

class Student():
    def __init__(self,name,age,sex,score=0):
        # 相当于调用了父类的方法
        # 指名道姓People
        People.__init__(self,name,age,sex)
        self.score = score
    def play(self):
        print('%s play football'%self.name)
class Teacher():
    def __init__(self,name,age,sex,hobby):
        # 相当于调用了父类的方法
        # 指名道姓People
        People.__init__(self,name,age,sex)
        self.hobby = hobby
    def course(self):
        print('%s course'%self.name)

s1 = Student('周阳',38,'male',99)
print(s1.__dict__)
t1 = Teacher('大海',18,'man','song')
print(t1.__dict__)
```

### 4 在单继承背景下的属性查找

```


# 在单继承背景下属性的查找优先级:对象->对象的类->父类->父类.....->object ******
# class Foo():
#     # xxx= 444
#     pass
#
# class Bar1(Foo):
#     # xxx = 333
#     pass
# #
# class Bar2(Bar1):
#     # xxx = 222
#     pass
# obj = Bar2()
# obj.xxx = 111
# print(obj.xxx)


class Foo:
    def f1(self):
        print('Foo.f1')

    def f2(self):
        print('Foo.f2')
        # obj.f1()是Bar()的对象
        self.f1()
class Bar(Foo):
    def f1(self):
        print('Bar.f1')
obj=Bar()
obj.f2()

'''
Foo.f2
Bar.f1
'''






```

### 5 在多继承背景下的属性查找

```
# 在多继承背景下属性的查找优先级:
# 此时属性的查找优先级是:对象->对象的类->按照从左往右的顺序一个分支一个分支的找下去
 # 广度优先查找,从左往右一个分支一个分支的查找,在最后一个分支才去查找顶级类
# 第四层
# 顶级类是在最后一个分之才走的
class G():
    # x = 'G'
    pass
# 第三层
class E(G):
    # x = 'E'
    pass
class F(G):
    # x='F'
    pass
# 第二层
class B(E):
    # x= "B"
    pass
class C(F):
    # x='C'
    pass
class D(G):
    # x='D'
    pass
# 第一层
class A(B,C,D):
    # x = 'A'
    pass
obj = A()

# obj.x = 111

# print(obj.x)
# python专门为继承类内置了一个mro的方法,用来查看c3算法的计算结果
# print(A.mro())
```

### 6 在子类派生的新方法中重用父类功能的方式二

```
'''
# 派生实例化除了父类的属性添加，还能有自己独有的属性
# 在子类派生出的新方法中重用父类功能的方式二:super()必须在类中用
# super(自己的类名,自己的对象)
# super()

'''
class People:
    sclool = '图灵学院'
    def __init__(self,name,age,sex):
        self.name=name
        self.age=age
        self.sex=sex
# s1 = People('周阳',38,'male')

class Student(People):
    def __init__(self,name,age,sex,score=0):
        # 相当于调用了父类的方法
        # 指名道姓People
        # People.__init__(self,name,age,sex)
        super(Student,self).__init__(name,age,sex)
        self.score = score
    def play(self):
        print('%s play football'%self.name)
class Teacher(People):
    def __init__(self,name,age,sex,hobby):
        # 相当于调用了父类的方法
        # 指名道姓People
        # People.__init__(self,name,age,sex)
        # 可以省略传值
        super().__init__(name, age, sex)
        self.hobby = hobby
    def course(self):
        print('%s course'%self.name)

s1 = Student('周阳',38,'male',99)
print(s1.__dict__)
t1 = Teacher('大海',18,'man','song')
print(t1.__dict__)


# 广度优先

class A:
    def f1(self):
        print('A.f1')

        super().f2()
class B:
    def f2(self):
        print('B.f2')
class C(A,B):
    def f2(self):
        print('C.f2')
obj=C()
obj.f1()
# C > A > B >object
print(C.mro())
'''
A.f1
B.f2
'''





```

### 7.组合

```
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





























```

### 8.多态

```
'''
1. 什么是多态
    多态指的是同一种/类事物的不同形态
2. 为何要用多态
    多态性:在多态的背景下,可以在不用考虑对象具体类型的前提下而直接使用对象
    多态性的精髓:统一
3. 如何用多态
'''
class Animal:
    # 动物都会叫
    def speak(self):
        print('我是动物我会说话')

class People(Animal):
    def speak(self):
        print('say hello')

class Dog(Animal):
    def speak(self):
        print('汪汪汪')

class Pig(Animal):
    def speak(self):
        print('哼哼哼')

# 三个对象都是动物

obj1=People()
obj2=Dog()
obj3=Pig()

# 多态性的精髓:统一
# 学车，学的是小汽车标准，会了所有的小汽车都会开
obj1.speak()
obj2.speak()
obj3.speak()

# 内置方法多态方法
# zhangdu()
# size()
# kuangdu()
# len()







```

### 9.常用的魔法方法

```
# __str__: 在对象被打印时自动触发,可以用来定义对象被打印时的输出信息

# class People:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
#     def __str__(self):
#         return 'name:%s,age%s'%(self.name,self.age)
# obj=People('大海',18)
# print(obj)

# __del__ 在对象被删除时先自动触发该方法,可以用来回收对象以外其他相关资源,比如系统资源

# class Foo:
# #     def __init__(self,x,filepath,encoding='utf-8'):
# #         self.x = x
# #         self.f = open(filepath,'rt',encoding=encoding)
# #     def __del__(self):
# #         print('测试')
# #         self.f.close()
# #
# # obj=Foo(1,'a.txt')
# # # 不是直接删除对象，只是调用__del__方法回收垃圾
# #
# # print(obj.f.read())

# __call__: 在对象被调用时会自动触发该方法

# class Foo:
#     def __init__(self,name,age):
#         self.name =name
#         self.age =age
#     def __call__(self, *args, **kwargs):
#         print(self)
#         print(args)
#         print(kwargs)
# obj=Foo(1,2)
# # 类里面没有__call__情况下对象不能调用
# # obj()
# obj()
# obj(1,2,a=3,b=4)














```

## 作业

```
'''
1.描述一下2种在子类派生的新方法中重用父类功能的方式。
2.定义一个矩形类，有长和宽两个实例/对象属性， 还有一个计算面积的方法
定义正方形类(继承矩形类)，实现类的实例/对象可调用，调用时打印正方形边长；
同时，直接打印类实例时能够打印出实例的面积，打印的这个面积会使用父类的方法。
'''
```