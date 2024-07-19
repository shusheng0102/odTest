class Mymeta(type):
    # 但凡继承了type的类才能称之为自定义的元类,否则就是只是一个普通的类
    # type(class_name,class_bases,class_dic)
    # __init__
    def __call__(self, *args, **kwargs):
        # self=Teacher这个类,args=('大海',18,'man'),kwargs={}
        print(self,args,kwargs)
        # 1. 先产生一个空对象__new__可以给Teacher这个类创建一个空对象
        # print('aaaa')
        tea_obj = self.__new__(self)
        # print(tea_obj)# tea_obj Teacher的对象 ， self Teacher
        # 2. 执行__init__方法,完成对象的初始属性操作
        self.__init__(tea_obj,*args, **kwargs)
        # 3. 返回初始化好的那个对象
        return tea_obj
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
    # def __call__(self, *args, **kwargs):
    #     print('aaaaa')
t=Teacher('大海',18,'man')
# print(Teacher.__dict__)
print(t.__dict__)
# t()
# 推理:如果一切皆对象,那么Teacher也是一个对象,
# 该对象之所可以调用,肯定是这个对象的类Mymeta中也定义了一个函数__call__









