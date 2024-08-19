import time

from flask import Flask, request, jsonify
from multiprocessing import Pool
import os

app = Flask(__name__)

# 定义一个多进程池
pool = Pool(processes=os.cpu_count())

# 假设的模型推理函数
def mock_model_inference(data):
    # 这里模拟推理过程，实际中应该是调用模型进行预测
    # 模拟模型推理耗时
    time.sleep(0.03)
    return "预测结果"

# 使用多进程池来执行模型推理
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # 使用apply_async异步执行模型推理，避免阻塞主线程
    result = pool.apply_async(mock_model_inference, (data,))
    # 等待结果返回
    result.wait()  # 这里可以设置超时时间
    return jsonify(result=result._value)

if __name__ == '__main__':
    # 使用Gunicorn的Worker类来运行Flask应用
    # 这里设置为gevent模式，也可以根据需要设置为sync模式
    from gunicorn.app.base import BaseApplication

    class FlaskApplication(BaseApplication):
        def init(self, parser, opts, args):
            return {
                'bind': '0.0.0.0:5000',
                'workers': os.cpu_count() * 2,  # 根据CPU核心数设置进程数
                'worker_class': 'gevent',  # 使用gevent作为worker
            }

        def load(self):
            return app

    application = FlaskApplication()
    application.run()