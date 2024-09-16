'''
1. 什么是多态
    多态指的是同一种/类事物的不同形态
2. 为何要用多态
    多态性:在多态的背景下,可以在不用考虑对象具体类型的前提下而直接使用对象
    多态性的精髓:统一
3. 如何用多态
'''
class Animal:
    # 动物都会叫
    def speak(self):
        print('我是动物我会说话')

class People(Animal):
    def speak(self):
        print('say hello')

class Dog(Animal):
    def speak(self):
        print('汪汪汪')

class Pig(Animal):
    def speak(self):
        print('哼哼哼')

# 三个对象都是动物

obj1=People()
obj2=Dog()
obj3=Pig()

# 多态性的精髓:统一
# 学车，学的是小汽车标准，会了所有的小汽车都会开
obj1.speak()
obj2.speak()
obj3.speak()

# 内置方法多态方法
# zhangdu()
# size()
# kuangdu()
# len()






