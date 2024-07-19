

# 在单继承背景下属性的查找优先级:对象->对象的类->父类->父类.....->object ******
# class Foo():
#     # xxx= 444
#     pass
#
# class Bar1(Foo):
#     # xxx = 333
#     pass
# #
# class Bar2(Bar1):
#     # xxx = 222
#     pass
# obj = Bar2()
# obj.xxx = 111
# print(obj.xxx)


class Foo:
    def f1(self):
        print('Foo.f1')

    def f2(self):
        print('Foo.f2')
        # obj.f1()是Bar()的对象
        self.f1()
class Bar(Foo):
    def f1(self):
        print('Bar.f1')
obj=Bar()
obj.f2()

'''
Foo.f2
Bar.f1
'''





