'''
Base64是网络上最常见的用于传输8Bit字节码的编码方式之一，
Base64就是一种基于64个可打印字符来表示二进制数据的方法。
定义     8Bit字节代码的编码方式之一
可用于    在HTTP环境下传递较长的标识信息
特性      Base64编码具有不可读性
# 它只是用传输，并不是加密
 Base64编码原理
    看一下Base64的索引表，字符选用了"A-Z、a-z、0-9、+、/" 64个可打印字符。
    数值代表字符的索引，这个是标准Base64协议规定的，不能更改。
'''
import base64
a = '大海'
a = a.encode('utf-8')
str_a=base64.b64encode(a)
print(str_a)
# 可以理解成一个中介
# 将base64解码成字符串
str_b = base64.b64decode(str_a).decode('utf-8')
print(str_b)



