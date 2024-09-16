# 错误
# import m2
# 绝对导入必须以执行文件为主
# from dir1 import m2
# # 没有前缀
# from dir1.m2 import f2
# 最正确方式用相对导入
from .m2 import f2
def f1():
    print('from f1')
    # 有前缀的绝对导入
    # m2.f2()
    # 无前缀的绝对导入
    f2()