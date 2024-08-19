import csv
import random
import time

import requests
from concurrent.futures import ThreadPoolExecutor

# Flask服务接口的URL
url = 'http://127.0.0.1:5000/write_csv'

# CSV文件路径
csv_filename = 'x.csv'

# 生成随机user_id的函数
def generate_random_user_id():
    return random.randint(1, 6040)
def read_and_send_row(filename, user_id):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        for row in reader:
            if row[1] == str(user_id):  # 假设user_id在第二列
                payload = {'headers': headers, 'data': row}
                try:
                    start_time = time.time()  # 请求开始时间
                    response = requests.post(url, json=payload, timeout=5)
                    response_time = time.time() - start_time  # 计算响应时间
                    print(f"请求{user_id}的响应时间: {response_time*1000:.4f}耗秒")
                    # return response.json()
                    response.raise_for_status()  # 检查请求是否成功
                    return True  # 请求成功
                except requests.exceptions.RequestException as e:
                    return False  # 请求失败

def main(concurrent_requests):
    success_count = 0
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
        futures = [executor.submit(read_and_send_row, csv_filename, generate_random_user_id()) for _ in range(concurrent_requests)]
        #results = [future.result() for future in futures]
        for future in futures:
            if future.result():
                success_count += 1  # 记录成功的请求

    end_time = time.time()
    total_time = end_time - start_time
    print(f"总耗时: {total_time:.2f}秒")
    print(f"TPS（每秒事务数）: {concurrent_requests / total_time}")

    # 检查响应结果
    # for result in results:
    #     if result.get('status') == 'success':
    #         print("数据写入成功")
    #     else:
    #         print("数据写入失败")
    total_requests = concurrent_requests
    success_rate = (success_count / total_requests) * 100
    print(f"成功率: {success_rate:.2f}%")

if __name__ == '__main__':
    concurrent_requests = 100  # 并发请求的数量
    main(concurrent_requests)