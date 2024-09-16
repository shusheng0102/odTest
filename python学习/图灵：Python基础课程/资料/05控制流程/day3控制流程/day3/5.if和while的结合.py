# 登录取款程序
# 理解while嵌套
user = '大海'
pwd = 123
balance = 5000
tag = True
while True:
    while tag:
        user1 = input('输入用户名')
        if user1 != user:
            print('你输入的用户名有错误，请重新输入')
            continue
        pwd1 = int(input('请输入密码'))
        if pwd == pwd1:
            print('登录成功')
            break
            # 跳出本层循环 ，也就是说这一层while tag循环直接结束
            # 虽然跳出了while tag:
            # 外面的while True还是又会进入while tag
        else:
            print('输入密码错误')
    # 目的只是为了不进入里面的循环
    # 下面我要写取款程序
    tag = False
    # print('走后面取款的代码')
    money = int(input('输入你的取款金额'))
    if balance > money:
        balance = balance - money
        print('恭喜你取走了%s'%money)
        print('还剩%s'%balance)
        break
    else:
        print('余额不足')