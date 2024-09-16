"""
    datetime
        python实现的一个时间处理模块
    time 用起来不太方便  所以就有了datetime
    总结 datetime相比time 更灵活 更本土化
"""
# import datetime
# print(datetime.datetime.now())

from datetime import datetime
# 获取时间 获取当前时间 并且返回的是格式化字符时间
print(datetime.now())
# 单独获取某个时间 年 月
d = datetime.now()
print(d.year)
print(d.month)
print(d.day)
print(d.minute)
print(d.second)
print(d.microsecond)
# 手动指定时间
print(datetime(2018,8,9,9,50,00))
d2 = datetime(2018,8,9,9,50,00)
print(d-d2)

# 替换某个时间单位的值
print(d.replace(year=2019))


