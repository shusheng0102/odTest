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




