from flask import Flask, Response

from app2 import run_by

app = Flask(__name__)

@app.route('/')
def index():
    return Response('hello')

if __name__ == '__main__':
    app.run()
    run_by()