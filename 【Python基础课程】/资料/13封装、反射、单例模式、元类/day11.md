## day11封装，反射，单例模式，元类

### 1.封装

```
'''
1. 什么是封装
    装:往容器/名称空间里存入名字
    封:代表将存放于名称空间中的名字给藏起来,这种隐藏对外不对内
2.为何要封装
    封数据属性:???
    封函数属性:???
3. 如何封装
    在类内定义的属性前加__开头(注意是2杠)
'''
class Foo:
    __x = 11
    __y = 22
    def __init__(self,name,age):
        self.__name = name
        self.age = age
    def __func(self):
        print('func')
    # 接口
    def get_info(self):
        print(self.__x,self.__y,self.__name)
        self.__func()

# # print(Foo.__x)
# # 1. __开头的属性到底如何实现的隐藏?
# # print(Foo.__dict__)
# # _类名__属性名
#
# # # 1. __开头的属性实现的隐藏仅仅只是一种语法意义上的变形,并不会真的限制类外部的访问
# # # 我们不这样做
# # print(Foo._Foo__x)
# # 误区封装是在定义类阶段进行的
# # # 该变形操作只在类定义阶段检测语法时发生一次,类定义阶段之后新增的__开头的属性并不会变形
# # Foo.__z =333
# # # print(Foo.__z)
# # print(Foo.__dict__)
#
# # 2. 如何实现的对外隐藏,对内不隐藏
# obj = Foo('大海',18)
# # obj.__func()
# obj.get_info()

class Foo:
    def __f1(self):#    _Foo__f1
        print('Foo.f1')

    def f2(self):
        print('Foo.f2')
        # obj.__f1()是Bar()的对象
        self.__f1()#    _Foo__f1 # 专属方法
        # self.__f1()   self._Foo__f1()  obj._Foo__f1   类定义的时候进行了统一
        #
        # self._Bar__f1()
class Bar(Foo):
    def __f1(self):#    _Bar__f1
        print('Bar.f1')
obj=Bar()
obj.f2()

'''
Foo.f2
Bar.f1
'''

```

### 2.封装属性的意义

```
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
```

### 3.封装方法的意义

```
# 封装函数属性:隔离复杂度  # 间接的访问一些不需要使用者知道的方法
class ATM:
    # 这些功能使用者没必要知道
    # 也就是说把类的内部没必要让使用者知道的功能封装起来
    def __card(self):
        print('插卡')
    def __auth(self):
        print('用户认证')
    def __input(self):
        print('输入取款金额')
    def __print_bill(self):
        print('打印账单')
    def __take_money(self):
        print('取钱')
        # 使用者只需要知道取款功能
        # 在类内部开一个统一的接口按步骤依次调用就可以了
    def withdraw(self):
        self.__card()
        self.__auth()
        self.__input()
        self.__print_bill()
        self.__take_money()
a=ATM()
a.withdraw()
```

### 4.property把方法封装成属性

```
'''
property是一种特殊的属性，访问它时会执行一段功能（函数）然后返回值  *****
例：BMI指数（bmi是计算而来的，但很明显它听起来像是一个属性而非方法，如果我们将其做成一个属性，更便于理解）
成人的BMI数值：
过轻：低于18.5
正常：18.5-23.9
过重：24-27
肥胖：28-32
非常肥胖, 高于32
　　体质指数（BMI）=体重（kg）÷身高^2（m）
'''
class People:
    def __init__(self,name,weight,height):
        self.name = name
        self.weight = weight
        self.height = height
    @property
    def bmi(self):
        return self.weight/(self.height**2)
obj = People('大海',70,1.75)
# print(obj.bmi())
# 把方法变成属性调用
print(obj.bmi)




```

### 5.反射

```
'''
反射:通过字符串来反射/映射到对象/类的属性上  *****
'''
class People:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def run(self):
        print('%s is running'%self.name)
obj = People('dahai',18)

# print(obj.__dict__)
# # 访问属性
# print(obj.name)
# # #obj.__dict__ 本质上就是在这个对象的字典里面找这个['name']
# print(obj.age)
# # 修改属性
# obj.name = 'dahai1'
# print(obj.__dict__)
# # # 删除属性
# del obj.name
# print(obj.__dict__)
# # 添加属性
# obj.sex = 'man'
# print(obj.sex)
# print(obj.__dict__)
# 让用户使用属性
# attr = input('用户输入属性').strip()
# print(type(attr))
# print(obj.name)
# obj.'name'
# 所以用户输入的是一个字符串的形式，我们怎样把它变成属性名，就用到了反射
# 判断对象是否有属性,有就返回True，没有就算False
# print(hasattr(obj,'name'))
#
# print(hasattr(obj,'aa'))
# 获取对象属性
# print(obj.name)
# print(getattr(obj,'name'))
# print(getattr(obj,'xxx',None))
# 第三个参数找不到返回None
# 修改对象属性
# setattr(obj,'name','dahai1')
# 修改了存在的
# print(getattr(obj,'name'))
# 不存在直接添加
# setattr(obj,'yyy',1111)

# print(obj.__dict__)
# 删除对象属性值
# delattr(obj,'name')
# print(obj.__dict__)
# print(hasattr(对象，'对象的属性'))
# 类也可以说是对象
# print(hasattr(类，'类的属性/或者方法'))
# print(hasattr(list,'append'))
# print(hasattr(list,'xxxx'))
# 反射方法应用
class ShoppingCart:
    def shopping(self):
        print('shopping')
    def login(self):
        print('login')
    def football(self):
        print('football')
    def run(self):
        cmd = input('请输入>>>').strip()
        # if cmd == 'login':
        #     self.login()
        # elif cmd == 'shopping':
        #     self.shopping()
        # 反射方法的作用
        if hasattr(self,cmd):
            # 拿到内存地址
            method = getattr(self,cmd)
            # print(method)
            # 调用s对象的方法
            method()
        else:
            print('输入的方法不存在')
s=ShoppingCart()
s.run()




```

### 6.单例模式

```
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






















```

### 7.什么是元类

```
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



























```

### 8.type元类创建自定义类

```
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
```

### 9.自定义元类

```
class Mymeta(type):
    # 但凡继承了type的类才能称之为自定义的元类,否则就是只是一个普通的类
    # type(class_name,class_bases,class_dic)
    # __init__
    def __init__(self,class_name,class_bases,class_dic):
        print(self)
        print(class_name)
        print(class_bases)
        print(class_dic)

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
t=Teacher('大海',18,'man')
```

### 10.自定义元类控制类的产生

```
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
```

### 11.自定义元类来控制类调用产生自定义对象

```
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










```

### 12.自定义元类来控制类的调用过程产生对象

```
'''
元类Mymeta实例化Teacher,调用Teacher实际上是调用元类Mymeta的__call__方法会
1. 先产生一个Teacher的空对象tea_obj
2. Teacher执行__init__方法,完成对象的初始属性操作
3. 返回初始化好的那个对象
推理:调用Teacher(...)就是在调用Teacher的元类Mymeta中的__call__,那么在该__call__中就需要做上述三件事
'''
# #自定义元类来控制类的调用(即类的实例化过程)
#1 我们把对象实例化的属性全部变成隐藏属性


class Mymeta(type):
    # 但凡继承了type的类才能称之为自定义的元类,否则就是只是一个普通的类
    # type(class_name,class_bases,class_dic)
    # __init__
    def __call__(self, *args, **kwargs):
        # self=Teacher这个类,args=('大海',18,'man'),kwargs={}
        # print(self,args,kwargs)
        # 1. 先产生一个空对象__new__可以给Teacher这个类创建一个空对象
        # print('aaaa')
        tea_obj = self.__new__(self)
        # print(tea_obj)# tea_obj Teacher的对象 ， self Teacher
        # 2. 执行__init__方法,完成对象的初始属性操作
        self.__init__(tea_obj,*args, **kwargs)
        # 在这里改
        # _类名__属性
        # print(tea_obj.__dict__)
        # 类名
        # print(self.__name__)
        # k1 = []
        # v1 = []
        # for k,v in tea_obj.__dict__.items():
        #     # print(k,v)
        #     # 形成了隐藏的语法效果
        #     # print('_%s__%s'%((self.__name__),k))
        #     # print(v)
        #     k1.append('_%s__%s'%((self.__name__),k))
        #     v1.append(v)
        # # print(k1)
        # # print(v1)
        # tea_obj.__dict__=dict(zip(k1,v1))
        # 字典生成式
        tea_obj.__dict__ = {'_%s__%s'%((self.__name__),k):v for k,v in tea_obj.__dict__.items()}
        # # 也可以加if判断
        # tea_obj.__dict__ = {'_%s__%s'%((self.__name__),k):v for k,v in tea_obj.__dict__.items()if v == '大海'}
        # 列表生成式
        print([i*i for i in range(1,10)])
        # 只拿到偶数
        print([i * i for i in range(1, 10)if i %2 ==0])
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



















```