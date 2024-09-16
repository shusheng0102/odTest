
# EMS (Employee Manager System) 练习

'''
命令行版本的员工管理系统
    1. 查询
    2. 添加
    3. 删除
    4. 退出

    -- 员工信息 存在列表中
    --
'''

print('-'*20, '欢迎使用员工管理系统', '-'*20)
# 创建一个列表，用来保存员工信息，员工的信息以字符串的形式统一保存到列表
emps = []

while True:
    print('请选择要做的操作：')
    print('\t1.查询员工\n\t2.添加员工\n\t3.删除员工\n\t4.退出系统')
    # print('\t2.添加员工')
    # print('\t3.删除员工')
    # print('\t4.退出系统')
    user_choose = input('请选择【1-4】：')
    print('-' * 58)
    # 根据用户的选择做相关操作
    if user_choose == "1":
        print('\t序号\t姓名\t年龄\t性别\t住址')
        for emp in emps:
            print(emp)
        pass
    elif user_choose == "2":
        pass
    elif user_choose == "3":
        pass
    elif user_choose == "4":

        print('欢迎使用本系统，再见！！！')
        input('点击回车退出！！！')
        break
    else :
        print('输入不符合要求，请重新选择')

    print('-'*58)

