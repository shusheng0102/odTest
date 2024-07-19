# 在python中统一了类与类型的概念
# class Foo:
#     def find(self):
#         print('我是绑定对象的方法')
# <class '__main__.Foo'>
# print(Foo)
# obj=Foo()
# print(obj)
# obj.find()
# <class '__main__.Foo'>
# print(type(obj))
# # ctrl 按住不动 点击鼠标左键
# print(str)
# # 其实python在'dahai'的前面自动加了一个str类
# name = str('dahai')
# print(type(name))
# # name变量名，name对象
# print(name.startswith('da'))


# 1 什么是元类:
# 源自一句话:在python中,一切皆对象,而对象都是由类实例化得到的
class Teacher:
    def __init__(self,name,age,sex):
        self.name = name
        self.age = age
        self.sex = sex
    def run(self):
        print('%s在跑步'%self.name)
t=Teacher('大海',18,'man')
# print(t)
# print(type(t))
# # 如果把Teather当做一个对象
# print(type(Teacher))
# 推理
# 对象t是调用Teacher类得到的,如果说一切皆对象,那么Teacher也是一个对象,只要是对象
# 都是调用一个类实例化得到的,即Teacher=元类(...),内置的元类是type

# 关系:
# 1. 调用元类---->自定义的类
# 2. 调用自定义的类---->自定义的对象


























