# 如果：成绩>=90，那么：优秀
#
# 如果成绩>=80且<90,那么：良好
#
# 如果成绩>=70且<80,那么：普通
#
# 其他情况：很差
score = int(input('>>>'))
if score >= 90:
    print('优秀')
if  90>score >= 80:
    print('良好')
if 80>score >= 70:
    print('普通')
if score < 70:
    print('很差')
# elif 与if并列的区别
# if并列是每个if都是独立的  也就是说每一个if条件 是独立的
# 而elif的条件  是在上个if 或者 上一个elif 不满足的条件下执行的条件
