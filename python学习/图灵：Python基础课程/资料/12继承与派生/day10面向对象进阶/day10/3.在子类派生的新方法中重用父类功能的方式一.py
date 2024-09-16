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