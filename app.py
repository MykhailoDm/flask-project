from flask import Flask

app = Flask(__name__)


@app.route('/hello-world-9')
def hello_world():
    return 'Hello World 9'


if __name__ == '__main__':
    app.run()
