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










