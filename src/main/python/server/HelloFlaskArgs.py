from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def print_string():
    input_string = request.args.get('key')
    if input_string:
        return f'You provided: {input_string}'
    else:
        return 'No string provided.'

if __name__ == '__main__':
    app.run()