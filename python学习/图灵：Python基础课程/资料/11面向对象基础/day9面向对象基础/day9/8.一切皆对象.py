# 在python中统一了类与类型的概念
class Foo:
    def find(self):
        print('我是绑定对象的方法')
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