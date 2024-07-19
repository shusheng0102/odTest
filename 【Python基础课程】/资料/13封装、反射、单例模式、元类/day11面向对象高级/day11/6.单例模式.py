'''
1、什么是单例模式  *****
    单：同一个
    例: 实例/对象
    模式：一个模板或者一个方法
    单例模式：基于某种方法实例化多次得到实例/对象是同一个
2、为何用单例模式
    当实例化多次得到的对象中（存放的属性）都（一样）的情况，应该将多个对象指向同一个内存，即同一个实例
3、如何用
'''
# 绑定类方法的单例模式
class Mysql:
    # 封装一下 对内不对外
    __instance = None
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
    @classmethod
    def from_conf(cls): # cls是Mysql这个类
        # print('绑定类方法')
        if cls.__instance is None:
            # print('=====')
            cls.__instance = cls('127.0.0.1',1234)# 完成Mysql对象的初始化 Mysql('127.0.0.1',1234)
            # print(cls.__instance)
        return cls.__instance
# 调用绑定的类方法
obj1=Mysql.from_conf()
obj2=Mysql.from_conf()
obj3=Mysql.from_conf()
print(id(obj1))
print(id(obj2))
print(id(obj3))
print(obj1)
print(obj2)
print(obj3)
print(obj1.ip)
print(obj2.ip)
print(obj3.ip)
# 调用类实例化
obj4=Mysql('192.168.65.111',5678)
print(obj4)
print(id(obj4))





















