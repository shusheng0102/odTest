# 拆包 *****
# 一个元素对应一个变量
a , b ,c= [1,2,3]
print(a)
print(b)
print(c)
# 多个元素对应一个变量
*a,b,c = [1,2,3,4,5,6]
print(a)
print(b)
print(c)
# 打散
print(*a)