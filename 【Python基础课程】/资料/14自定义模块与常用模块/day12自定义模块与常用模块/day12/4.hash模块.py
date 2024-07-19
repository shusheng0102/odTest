# 1、什么叫hash:hash是一种算法，该算法接受传入的内容，经过运算得到一串hash值
# 2、hash值的特点是： *****
#2.1 只要传入的内容一样，得到的hash值必然一样=====>文件完整性校验
#2.2 不能由hash值返解成内容=======》把密码做成hash值，不应该在网络传输明文密码
#2.3 只要使用的hash算法不变，无论校验的内容有多大，得到的hash值长度是固定的,这样不影响传输

import hashlib
# # # 1创建hash工厂
# m=hashlib.md5()
# # # 运输的是二进制
# # # 2在内存里面运送
# # m.update('helloworld'.encode('utf-8'))
# # # 一点一点的给，因为可能二进制会很长 ,这个要好一些
# m.update('hello'.encode('utf-8'))
# m.update('world'.encode('utf-8'))
#
# # # 3、产出hash值
# print(m.hexdigest())
# # fc5e038d38a57032085441e7fe7010b0

# m=hashlib.md5()
#
# with open(r'D:\python代码2\day10\基础继承.png','rb')as f:
#     for line in f:
#         m.update(line)
#     hv = m.hexdigest()
# print(hv)
# 输入密码的时候是沿着网络传输到别的服务器上面，黑客可以把包抓下来
# 所以发给服务端是hash值，也就是密文
# 但是还是可以抓下来
# 常用密码字典
# 什么生日 ， 123 ， 身份证  等等 密码有强烈的个人习惯
# 那么我用一样的hash算法，是不是可以得到一样的hash值  密文  那么明文肯定是一样的
# 撞库风险

# 密码前后加盐
# pwd = 'abc123'
#
# m = hashlib.md5()
# m.update('大海老师'.encode('utf-8'))
# m.update('pwd'.encode('utf-8'))
# m.update('夏洛特烦恼'.encode('utf-8'))
#
# print(m.hexdigest())
# 服务器也有相应的规则
# 黑客破解成本远大于收益成本
# 中间加盐

# import  hashlib
# pwd = 'abc123'
# print(pwd[0])
# print(pwd[1:])
# m = hashlib.md5()
# m.update('大海老师大帅比'.encode('utf-8'))
# m.update(pwd[0].encode('utf-8'))
# m.update('夏洛特'.encode('utf-8'))
# m.update(pwd[1:].encode('utf-8'))
# m.update('烦恼'.encode('utf-8'))
# print(m.hexdigest())


#2.3 只要使用的hash算法不变，无论校验的内容有多大，得到的hash值长度是固定的,这样不影响传输
m=hashlib.md5()
# # 运输的是二进制
# # 2在内存里面运送
m.update('helloworldaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))


# # 3、产出hash值
print(m.hexdigest())
# fc5e038d38a57032085441e7fe7010b0
# 38f317ec47937721411bdca9ac00c081
# sha后面的数字越大加密的算法越复杂
m1=hashlib.sha256()
m1.update('helloaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))
print(m1.hexdigest())
# 9abfe77d5eb12f4a1012ac1407ce8aeb73b76803caf2092247777b1a70cc118e
# f683dd28f66cd8b5042b66b39c192e93485d98a80f7ae8e04924b378b96ff4ea
m2=hashlib.sha512()
m2.update('helloaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'.encode('utf-8'))
print(m2.hexdigest())
# 1c71f4e620ec0b0824b1e6dfdfa808c4103b4f86c61b422bef55270c830eff5a6c7de5068c500898c35d0c2c1e8bd326696d05d4ac9919dcf8dcd68278c11982
# d030dba5eeb0381eae8e8f9d8ab7eab0963bb3a43a18fc48190d4101d1190f89e3d72e6fbc4abc81264af2ac83dc38108eff722369c276ec47f504a5345cb81e