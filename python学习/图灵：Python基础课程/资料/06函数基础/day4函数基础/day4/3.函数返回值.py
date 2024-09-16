# 什么是返回值？
# L = [1,2,3,4]
# # n=L.pop()
# # print(L)
# # print(n)
# 返回值是一个函数的处理结果（物流）return
# 函数属于局部
'''
注意：
        1、return是一个函数结束的标志，函数内可以有多个return，
            但只要执行一次，整个函数就会结束运行
            默认return None  *****
        2、return 的返回值无类型限制，即可以是任意数据类型  *****
        3、return 的返回值无个数限制，即可以用逗号分隔开多个任意类型的值  *****
            0个：返回None，ps：不写return默认会在函数的最后一行添加return None
            1个:返回的值就是该值本身
            多个：返回值是元组
        4.return关键字:return也可以作为函数结束的标志, ****
#         那么利用这一点就可以结束循环
'''
# def factory(a):
#     #这个是在函数里面用的，工厂里面自己用
#     # c = a + 1
#     # print(c)
#     if a == 1:
#         return [1,2,3],True,'aaaa'
#     # print('制造手机')
#     # return 2
#     # return 1
#     # print('制造电脑')
#     # return 2
#     # return c
#     # return None
# a=factory(1)
# print(a)

# 4.return关键字:return也可以作为函数结束的标志, ****
#         那么利用这一点就可以结束循环
def factory(a):
    print('======')
    print('======')
    print('======')
    while True:
        while True:
            while True:
                if a == 3:
                    return
                a += 1
                print(a)
factory(1)



