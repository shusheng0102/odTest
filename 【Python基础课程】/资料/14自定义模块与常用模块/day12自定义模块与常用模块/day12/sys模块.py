"""
    sys模块
    sys模块是与python解释器交互的一个接口
"""
import sys
# sys.path   返回模块的搜索路径，初始化时使用PYTHONPATH环境变量的值

print(sys.path)
sys.path.append('D:\python代码2\day12\dir0')
print(sys.path)
from dir2 import aaaaa

aaaaa.a()