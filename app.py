from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/fitbit/callback", methods=["GET"])
def fitbit():
    return "<h1>Test Flask App</h1>"


if __name__ == "__main__":
    app.run()