#逻辑运算and or not
# and 与:连接左右两个条件,只有在两个条件同时成立的情况下最终结果才为True
# 快速判断方法
# 全部都是and的情况下，如果判断到位假后面都是and就没必要看了，就是假
# 要求全部都是真才是真
name = 'dahai'
num = 20
print(num > 18 and 1>3 and name == 'dahai' and num < 26)
print(num > 18 and 3>1 and name == 'dahai' and num < 26)

# or 或:连接左右两个条件,但凡有一个条件成立最终结果就为True
# 快速判断方法
# 全部都是or的情况下，如果判断到位真后面都是or就没必要看了，就是真
# 全是假才是假
print( 1>3or 1 ==1 or 'x'== 'y' or 2 > 4)
# not 非
print(not 1 > 3)
'''
原理为：
(1) not的优先级最高，就是把紧跟其后的那个条件结果取反，所以not与紧跟其后的条件不可分割

(2) 如果语句中全部是用and连接，或者全部用or连接，那么按照从左到右的顺序依次计算即可

(3) 如果语句中既有and也有or，那么先用括号把and的左右两个条件给括起来，然后再进行运算
'''
print(not 3 > 1 or 3 >1)
#  是先判断not 3>1  而不是 3>1 or 3>1
# not 相当于小学学的乘除法  ，and和or相当于加减法
res=not False and True or False or False or True
# #2、最好使用括号来区别优先级，这样别人容易读懂你的代码
res1 =  (3>4 and 4>3) or (1==3 and ('x'=='x' or 3>3))
print(res1)