# class Teacher:
#     HP = 100
#     def __init__(self,name,age,sex):
#         self.name = name
#         self.age = age
#         self.sex = sex
#     def run(self):
#         print('%s在跑步'%self.name)
# t=Teacher('大海',18,'man')
# print(type(Teacher))
# 自定义类的三个关键组成部分:
# 1. 类名
# 2. 类的基类们 object
# 3. 类的名称空间
'''

class关键字创建自定义类的底层的工作原理,分为四步
1. 先拿到类名:'Teacher'
2. 再拿到类的基类们:(object,)
3. 然后拿到类的名称空间???(执行类体代码,将产生的名字放到类的名称空间也就是一个字典里,补充exec)
4. 调用元类实例化得到自定义的类：Teacher=type('Teacher',(object,),{...})
'''
# 不依赖class关键字创建一个自定义类
# 1. 拿到类名
class_name = 'Teacher'
# #2. 拿到类的基类/父类们:(object,)
class_bases = (object,)
#3. 拿到类的名称空间  类的属性 ，方法   也就是类的体代码
class_body = '''
HP = 100
def __init__(self,name,age,sex):
    self.name = name
    self.age = age
    self.sex = sex
def run(self):
    print('%s在跑步'%self.name)
'''
class_dic = {}
# 介绍 exec 函数   可以执行字符串里面的代码
# exec('print(1)')
# exec函数的使用，第一个参数代码放到字符串里面，第二个参数是全局的字典，第三个参数的局部的字典
# exec('x=1',{},{})
# exec函数的使用，我要用第一个参数代码放到字符串里面，不用第二个参数是全局的字典因为类体代码没有这样的需求
# ，用第三个参数的局部的字典
exec(class_body,{},class_dic)
# 4. 调用元类实例化得到自定义的类：Teacher=type('Teacher',(object,),{...})
Teacher=type(class_name,class_bases,class_dic)
print(Teacher)
print(Teacher.HP)
print(Teacher.run)
a=Teacher('dahai',18,'man')
a.run()