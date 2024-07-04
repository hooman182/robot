from flask import Flask, Response

from myBot import run_by

app = Flask(__name__)

@app.route('/')
def index():
    return Response('hello')

run_by()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)