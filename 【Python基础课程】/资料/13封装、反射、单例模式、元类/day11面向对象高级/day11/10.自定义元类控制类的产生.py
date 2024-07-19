'''
现在可以控制类的产生
1.类名必须用驼峰体
2.类体必须有文档注释,且文档注释不能为空
'''
class Mymeta(type):
    # 但凡继承了type的类才能称之为自定义的元类,否则就是只是一个普通的类
    # type(class_name,class_bases,class_dic)
    # __init__
    def __init__(self,class_name,class_bases,class_dic):
        if class_name.islower():
            raise TypeError('类名必须使用驼峰体')
        # print(class_dic.get('__doc__'))
        doc=class_dic.get('__doc__')
        if doc is None or len(doc)==0 or len(doc.strip('\n '))==0:
            raise TypeError('类体必须有文档注释,且文档注释不能为空')
    #  '__doc__': None
# 这里必须写object ，默认的type元类会做，自定义元类的要自己写
class Teacher(object,metaclass=Mymeta):
    '''
    aaaa
    '''
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
# print(Teacher.__dict__)