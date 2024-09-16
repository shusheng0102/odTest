#语法1：
# if 条件:
#     代码体
#     code1
#     code2
#     code3
#     ....
# 语法记忆方法
#   if+空格+条件+冒号
#   tab缩进代码体
#   tab缩进代码体
#   tab缩进代码体
# 键盘Q 左边tab
#  代表电脑需要一个条件进行判断  冒号可以理解成代表计算机要说话了
#  那么通过tab横向换行确定要说的话
# tag = False
# if tag:
#     print('条件满足')
#     print('条件满足')
#     print('条件满足')
#语法2：
# if 条件:
#     代码体
#     code1
#     code2
#     code3
#     ....
#else:
#     代码体
#     code1
#     code2
#     code3
# tag = 1 == 3
# if tag:
#     print('条件满足')
#     print('条件满足')
#     print('条件满足')
# # 其他
# else:
# # tab 右边缩减  shift + tab 左边缩进
#     print('条件不满足')
#     print('条件不满足')
#语法3：多分枝
# 强调：if的多分枝=但凡有一个条件成立，就不会再往下判断其他条件了
# elif可以有无限个
# if 条件1:
#     code1
#     code2
#     code3
#     ....
# elif 条件2:
#     code1
#     code2
#     code3
#     ....
# elif 条件3:
#     code1
#     code2
#     code3
#     ....
# ........
# else:
#     code1
#     code2
#     code3
#     ....

# 优先级if最高  elif 依次从上往下 else
# 注意必须要有if
# 如果：成绩>=90，那么：优秀
#
# 如果成绩>=80且<90,那么：良好
#
# 如果成绩>=70且<80,那么：普通
#
# 其他情况：很差

# score = int(input('>>>'))
# if score >= 90:
#     print('优秀')
# elif score >= 80:
#     print('良好')
# elif score >= 70:
#     print('普通')
# elif score <70:
#     print('很差')
# 等价
# else:
#     print('很差')
# if 嵌套
# 语法
# if 条件:
#     code1
#     code2
#     code3
#     if 条件:
#           code1
#           code2
#           code3
#     else:
#           code1
#           code2
#           code3
# else:
#     code1
#     code2
#     code3
#     if 条件:
#           code1
#           code2
#           code3
#     else:
#           code1
#           code2
#           code3
cls = 'human'
sex = 'female'
age = 20
# 条件都要满足
if cls =='human' and sex == 'female' and age > 18 and age < 26:
    print('开始表白..... 以下省略一万字')
    is_success = input('女孩输入我愿意')
    # 嵌套里面当然也是可以用if 语法 1 2 3
    if is_success == '我愿意':
        print('在一起')
    else:
        print('我逗你玩呢....')
else:
    print('姐姐好')

























