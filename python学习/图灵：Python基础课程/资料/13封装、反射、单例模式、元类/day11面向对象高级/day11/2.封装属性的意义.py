# # 封装数据属性:将数据属性隐藏起来,类外就无法直接操作属性,怎么间接使用？ *****
# # 需要类内开辟一个接口来外部的使用可以间接地操作属性,可以在接口内定义任意的控制逻辑,
# # 从而严格控制使用对属性的操作
class People:
    def __init__(self,name,age):
        self.__name = name
        self.__age = age
    def tell_info(self):
        print('name:%s age:%s'%(self.__name,self.__age))
    def set_info(self,name,age):
        if type(name) is not str:
            print('名字必须为字符串')
            return
        if type(age) is not int:
            print('年龄必须为整型')
            return
        self.__name = name
        self.__age = age
obj = People('大海',18)
# 严格的控制查看属性
# print(obj.__name)
# 可以通过接口间接的访问到属性
obj.tell_info()
# 严格的控制修改属性
# obj.__name = 1232131
# obj.set_info(111,22)
# 必须名字必须为字符串，年龄必须为整型
obj.set_info('夏洛',22)
# 访问修改后的属性
obj.tell_info()