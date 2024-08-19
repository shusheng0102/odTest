import requests
import csv

#data = "value1,value2,value3"

# 假设CSV文件名为data.csv
# csv_filename = 'x.csv'
#
# # 打开CSV文件
# with open(csv_filename, mode='r', encoding='utf-8') as file:
#     # 创建CSV阅读器
#     reader = csv.reader(file)
#
#     # 读取表头（如果需要）
#     headers = next(reader)
#
#     # 遍历CSV文件中的每一行
#     for row in reader:
#         # 检查user_id是否等于230
#         if row[1] == '410':  # 假设user_id在第二列
#             print(f"找到匹配的行: {row}")
#             data = "|".join(row.values())
#             break  # 找到匹配的行后退出循环
# response = requests.post("http://127.0.0.1:5000/", data={'string': data})
#
# print(response.text)

def find_user_id(filename, user_id):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        for i, row in enumerate(reader):
            if row[1] == str(user_id):  # 假设user_id在第二列
                return headers, row
    return None, None

# 使用函数查找user_id=230的行
headers, user_data = find_user_id('x.csv', 230)
if user_data:
    print(f"表头: {headers}")
    print(f"找到的数据: {user_data}")
else:
    print("未找到user_id=230的数据")

def send_to_flask_service(headers, data):
    url = 'http://127.0.0.1:5000/write_csv'  # Flask服务接口的URL
    payload = {'headers': headers, 'data': data}
    response = requests.post(url, json=payload)
    return response.json()

# 发送数据到Flask服务
result = send_to_flask_service(headers, user_data)
print(result)