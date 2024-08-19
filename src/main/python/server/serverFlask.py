from flask import Flask, request, jsonify
import time  # 用于模拟模型推理时间

app = Flask(__name__)

# 假设的模型推理函数
def mock_model_inference(data):
    # 这里模拟推理过程，实际中应该是调用模型进行预测
    time.sleep(0.03)  # 模拟模型推理耗时30ms
    return "预测结果"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    result = mock_model_inference(data)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)