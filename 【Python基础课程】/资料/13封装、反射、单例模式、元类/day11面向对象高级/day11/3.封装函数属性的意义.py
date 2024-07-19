# 封装函数属性:隔离复杂度  # 间接的访问一些不需要使用者知道的方法
class ATM:
    # 这些功能使用者没必要知道
    # 也就是说把类的内部没必要让使用者知道的功能封装起来
    def __card(self):
        print('插卡')
    def __auth(self):
        print('用户认证')
    def __input(self):
        print('输入取款金额')
    def __print_bill(self):
        print('打印账单')
    def __take_money(self):
        print('取钱')
        # 使用者只需要知道取款功能
        # 在类内部开一个统一的接口按步骤依次调用就可以了
    def withdraw(self):
        self.__card()
        self.__auth()
        self.__input()
        self.__print_bill()
        self.__take_money()
a=ATM()
a.withdraw()