import json
# 反序列化
#             loads 处理字符串
#             load  处理文件
#反序列化：中间格式json-----》内存中的数据类型
# # loads(json格式字符串)
# with open('db.json','rt',encoding='utf-8')as f:
#     json_str = f.read()
#     print(json_str)
# # #2、将json_str转成内存中的数据类型
#     dic = json.loads(json_str)
#     print(dic,type(dic))
# load(json文件对象)
#1和2可以合作一步
with open('db.json','rt',encoding='utf-8')as f:
    dic=json.load(f)
    print(dic, type(dic))


