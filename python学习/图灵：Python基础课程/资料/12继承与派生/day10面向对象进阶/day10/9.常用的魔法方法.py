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













