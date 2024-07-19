# 在多继承背景下属性的查找优先级:
# 此时属性的查找优先级是:对象->对象的类->按照从左往右的顺序一个分支一个分支的找下去
 # 广度优先查找,从左往右一个分支一个分支的查找,在最后一个分支才去查找顶级类
# 第四层
# 顶级类是在最后一个分之才走的
class G():
    # x = 'G'
    pass
# 第三层
class E(G):
    # x = 'E'
    pass
class F(G):
    # x='F'
    pass
# 第二层
class B(E):
    # x= "B"
    pass
class C(F):
    # x='C'
    pass
class D(G):
    # x='D'
    pass
# 第一层
class A(B,C,D):
    # x = 'A'
    pass
obj = A()

# obj.x = 111

# print(obj.x)
# python专门为继承类内置了一个mro的方法,用来查看c3算法的计算结果
# print(A.mro())