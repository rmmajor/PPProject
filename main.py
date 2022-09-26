from flask import Flask

app = Flask(__name__)


@app.route("/")
def test():
    return 'Hello, world!'


@app.route("/api/v1/hello-world-8")
def lab():
    return 'Hello, world-8'


if __name__ == '__main__':
    app.run(debug=True)