import pandas as pd
import torch
from flask import Flask, request, jsonify
import csv

from src.main.python.server.csv_flask_load_data.dataset import DatasetV2
from src.main.python.server.csv_flask_load_data.features import movielens_seq_features_from_row

app = Flask(__name__)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    # data = request.get_data(as_text=True)
    # if data:
    #     with open('data.csv', 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile)
    #         row_data = [item.strip() for item in data.split('|')]
    #         writer.writerow(row_data)
    #     return 'Data written successfully.'
    # else:
    #     return 'No data provided.'
    data = request.json
    headers = data['headers']
    user_data = data['data']
    data_frame = pd.DataFrame([user_data], columns=headers)
    # 写入本地CSV文件
    eval_dataset = DatasetV2(
        data_frame=data_frame,
        padding_length=200 + 1,  # target
        ignore_last_n=0,
        chronological=True,
        sample_ratio=1.0,  # do not sample
    )
    data_loader = torch.utils.data.DataLoader(
        eval_dataset,
        batch_size=1,
        # shuffle=True, cannot use with sampler
        shuffle=False,
        num_workers=3,
        sampler=None,
        prefetch_factor=128,
    )
    device = torch.device("cpu")
    for eval_iter, row in enumerate(iter(data_loader)):
        seq_features, target_ids, target_ratings = movielens_seq_features_from_row(
            row, device=device, max_output_length=10 + 1
        )
        print(target_ids)
        print(seq_features.past_ids)

    return jsonify({'code': '0', 'status': 'success', 'message': '数据写入成功'})
if __name__ == '__main__':
    app.run(debug=True)