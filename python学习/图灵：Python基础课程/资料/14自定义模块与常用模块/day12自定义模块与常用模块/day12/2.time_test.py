"""
    time模块
        与时间相关的功能
    在python中 时间分为3种
        1.时间戳  timestamp  从1970 年 1 月 1日 到现在的秒数  主要用于计算两个时间的差
        2.localtime  本地时间  表示的是计算机当前所在的位置
        3.UTC 世界协调时间 又称世界统一时间、世界标准时间、国际协调时间。
          时间戳 结构化 格式化字符
"""
import time
# 获取时间戳 返回的是浮点型
# 作用 用来计算时间差
print(time.time())
# 获取当地时间   返回的是结构化时间
print(time.localtime())
#  获取UTC时间 返回的还是结构化时间  比中国时间少8小时
print(time.gmtime())
# # 结构化时间转换成字符串时间
print(time.strftime('%Y-%m-%d %H:%M:%S'))
# 将格式化字符串的时间转为结构化时间  注意 格式必须匹配
print(time.strptime('2021-05-24 20:44:18','%Y-%m-%d %H:%M:%S'))

# 时间戳 转结构化
# 10秒时间戳
print(time.localtime(10))
# 当前时间戳
print(time.localtime(time.time()))
# 结构化转 时间戳
print(time.mktime(time.localtime()))
# sleep
# 让当前进程睡眠一段时间 单位是秒
time.sleep(1)
print('over')
