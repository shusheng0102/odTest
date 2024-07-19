class Mymeta(type):
    # 但凡继承了type的类才能称之为自定义的元类,否则就是只是一个普通的类
    # type(class_name,class_bases,class_dic)
    # __init__
    def __init__(self,class_name,class_bases,class_dic):
        print(self)
        print(class_name)
        print(class_bases)
        print(class_dic)

class Teacher(object,metaclass=Mymeta):
    # Teacher=type('Teacher',(object,),{...})
    # #Teacher=Mymeta('Teacher',(object,),{...})
    HP = 100
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    def run(self):
        print('%s在跑步'%self.name)
t=Teacher('大海',18,'man')