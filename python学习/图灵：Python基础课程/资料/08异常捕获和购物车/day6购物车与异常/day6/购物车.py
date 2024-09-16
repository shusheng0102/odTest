# 业务逻辑
# python基础70%     40分钟写出来 优秀    1小时  良好    1个半小时 及格    不超过3个报错
# 1先听懂 全部写成文字信息
# 2根据文字信息开始写
import time
user_dic = {
    'name':'大海',
    'password':123,
    'locked':False,
    'account':50000,
    'shopping_cart':{}
}
def login():
    '''
    登录函数，密码输入错误3次锁定5秒，用户名输入错误可以一直输入
    :return:
    '''
    print('请登录')
    count = 0
    while True:
        # 'locked':False,一开始是非锁定的
        if user_dic['locked']:
            print('你已经输入密码错误3次,系统锁定5秒,请等待5秒后再登录')
            #  sleep(5) 秒
            time.sleep(5)
            user_dic['locked']=False
            count=0
        name = input('输入用户名').strip()
        if name == user_dic['name']:
            pwd = int(input('输入密码').strip())
            if user_dic['password']==pwd and user_dic['locked']==False:
                print('登录成功')
                break
            else:
                print('密码错误')
                count += 1
        else:
            print('用户名不存在')
        if count >= 3:
            user_dic['locked']=True
# login()
def login_intter(func): # shopping   func
    def wrapper():
        login()
        func()
    return wrapper




@login_intter
def shopping():
    print('购物')
    goods_list = [
        ['coffee', 30],
        ['chicken', 20],
        ['iPhone', 10000],
        ['car', 100000],
        ['building', 200000],
    ]
    shopping_cart = {}
    cost_money = 0
    while True:
        # 展示商品
        # enumerate 枚举
        for i,item in enumerate(goods_list):
            # 商品序号， [商品名，商品价格]
            # i就是列表的索引
            # item就是列表的元素
            print(i,item)
        choice=input('输入商品对应的编号,按t键结账').strip()
        # input输入的是数字吗？字符串的数字
        if choice.isdigit():
            # 判断字符串是否是数字
            # 进入了这个里面，字符串的数字
            choice = int(choice)
            if choice < 0 or choice >= len(goods_list):
                print('请选择相应的编号')
                continue
            goods_name=goods_list[choice][0]
            goods_price=goods_list[choice][1]
            # print(goods_name)
            # print(goods_price)
            if user_dic['account'] >= goods_price:
                if goods_name in shopping_cart:
                    # print('第二次添加同样商品')
                    # print('第三次添加同样商品')
                    # ....
                    shopping_cart[goods_name]['count']+=1
                    # print(shopping_cart)
                else:
                    # print('第一次添加同样商品')
                    shopping_cart[goods_name]={'price':goods_price,'count':1}
                    # print(shopping_cart)# {'chicken': {'price': 20}}
                #
                # 账户的金额 = 账户的金额 - 商品的价格
                user_dic['account'] -= goods_price
                # 花费的金额 =  花费的金额(一开始是0) + 商品的价格
                cost_money += goods_price
                # 提示用户这一次你加入购物车的商品名字
                print('%s 新的购物商品'%goods_name)
            else:
                print('钱不够')
        elif choice == 't':
            print(shopping_cart)
            buy = input('买不买(y/n)>>>').strip()
            if buy == 'y':
                if cost_money == 0:
                    print('不买，白看')
                    break
                # 把购物车的信息存到用户信息里面去
                user_dic['shopping_cart'] = shopping_cart
                print('%s 花费了%s 购买了%s'%(user_dic['name'],cost_money,shopping_cart))
                print('账号信息%s'%user_dic)
                break
            else:
                print('不买')
                break
        else:
            print('非法输入')
shopping()














