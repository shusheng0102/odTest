from flask import Flask, request, jsonify
import csv

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
    # 写入本地CSV文件
    with open('output.csv', mode='a', newline='', encoding='utf-8') as file:
        '''
        在Python的文件操作中，mode='a'表示以追加模式打开文件。这意味着如果文件已经存在，写入操作会在文件的末尾添加内容，而不是覆盖原有内容。如果文件不存在，它会被创建。

        除了'a'之外，还有一些其他的模式可以用于打开文件：
        
        'r'：读取模式，默认值。如果文件不存在，抛出异常。
        'w'：写入模式。如果文件存在，会被覆盖。如果文件不存在，会被创建。
        'x'：独占创建模式。如果文件已存在，无法创建，会抛出异常。
        'b'：二进制模式。用于读写二进制文件，如图片、音频等。
        't'：文本模式（默认值）。用于读写文本文件。
        '+'：更新模式。可以读写文件。如果与'r'、'w'或'a'结合使用，可以打开文件进行读取和写入。
        例如：
        
        'r+'：读写模式，文件必须存在。
        'w+'：读写模式，如果文件存在，会被覆盖；如果文件不存在，会被创建。
        'a+'：读写模式，用于追加。如果文件存在，写入操作会在文件末尾添加内容；如果文件不存在，会被创建。
        在使用'a'或'a+'模式时，如果你想要确保表头只写一次，可以在写入之前检查文件的大小或者使用文件指针file.seek(0)来检查文件是否为空。如果文件为空，那么写入表头，然后写入数据。如果文件不为空，只需追加数据即可。
        '''
        writer = csv.writer(file)
        # 如果文件是空的，写入表头
        if file.tell() == 0:
            writer.writerow(headers)
        # 写入找到的数据
        writer.writerow(user_data)

    return jsonify({'code': '0', 'status': 'success', 'message': '数据写入成功'})
if __name__ == '__main__':
    app.run(debug=True)