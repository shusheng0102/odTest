import os

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
# 定义员工信息文件的路径
EMP_FILE = 'emps.txt'

# 读取员工信息
def read_emps():
    if not os.path.exists(EMP_FILE):
        # 文件不存在，创建文件并写入标题
        write_emps('孙悟空1\t500\t男\t花果山')
        write_emps('孙悟空2\t300\t男\t花果山')
    with open(EMP_FILE, 'r', newline='', encoding='utf-8') as file:
        context = file.readlines()
        emps = [row.replace('\n', '') for row in context]
    return emps

# 写入员工信息
def write_emps(emp):
    with open(EMP_FILE, 'a', newline='', encoding='utf-8') as file:
        file.write(emp + '\n')

def write_all_emps(emps):
    with open(EMP_FILE, 'w', newline='', encoding='utf-8') as file:
        for emp in emps:
            file.write(emp + '\n')

print('-'*20, '欢迎使用员工管理系统', '-'*20)
# 创建一个列表，用来保存员工信息，员工的信息以字符串的形式统一保存到列表
# emps = ['\t1\t孙悟空\t500\t男\t花果山']
# 从本地文件中读取员工信息放入emps，列之间以\t分割
emps = read_emps()

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
        id = 1
        for emp in emps:
            print(f'\t{id}\t{emp}')
            id += 1


    elif user_choose == "2":
        # 添加员工
        # 获取要添加员工的信息、年龄、性别、住址
        emp_name = input('请输入新员工的姓名：')
        emp_age = input('请输入新员工的年龄：')
        emp_gender = input('请输入新员工的性别：')
        emp_address = input('请输入新员工的住址：')
        # 创建员工信息
        # 将四个信息拼接为一个字符串，然后插入到列表中
        emp = f'{emp_name}\t{emp_age}\t{emp_gender}\t{emp_address}'
        # 显示提示信息
        print('以下员工将被添加到系统中')
        print('-' * 58)
        print('\t序号\t姓名\t年龄\t性别\t住址')
        print('\t', emp)
        print('-' * 58)
        user_confirm = input('是否确认该操作【Y/N】：')
        if user_confirm.lower() == 'y' or user_confirm.lower() == 'yes':
            emps.append(emp)
            print('添加成功！')
            write_emps(emp)
        else:
            print('添加已取消！')
    elif user_choose == "3":
        # 删除员工想，根据员工的序号来删除员工
        # 获取要删除的员工的序号
        check_no_ok = True
        while check_no_ok:
            del_id = int(input('请输入要删除的员工序号：'))
            if del_id < 1 or del_id > len(emps):
                print('输入不合法，请重新输入！')
            else:
                break
        # 列表是0开始的，所以需要 -1
        del_emp = emps[del_id - 1]
        # 显示提示
        print('-' * 58)
        print('\t序号\t姓名\t年龄\t性别\t住址')
        print(f'\t{del_id}\t{del_emp}')
        print('-' * 58)
        user_confirm = input('该操作不可恢复，是否确认该操作【Y/N】：')
        if user_confirm.lower() == 'y' or user_confirm.lower() == 'yes':
            emps.remove(del_emp)
            write_all_emps(emps)
            print('删除成功！')
        else:
            print('删除已取消！')
    elif user_choose == "4":

        print('欢迎使用本系统，再见！！！')
        input('点击回车退出！！！')
        break
    else :
        print('输入不符合要求，请重新选择')

    print('-'*58)

