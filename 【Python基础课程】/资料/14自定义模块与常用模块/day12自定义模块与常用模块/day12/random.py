"""
    random 随机数相关模块

"""
import random
# 0 - 1 随机浮点 不包含1 random 0-1 开闭
print(random.random())
# randint 1 - 3 开开 整型
print(random.randint(1,3))
# randrange 1 - 3 开闭

print(random.randrange(1,3))
# 随机选⼀个
print(random.choice([1,2,3]))
# 随机选指定个数sample(列表，指定列表的个数)
print(random.sample([1,2,3],2))
# 打乱顺序shuffle(列表)
l = [1,2,3,4,5]
random.shuffle(l)
print(l)
# 闭闭 浮点
print(random.uniform(1,2))

# 作业
# 生产验证码函数 整形和字母大小写随机组成  可以指定长度




