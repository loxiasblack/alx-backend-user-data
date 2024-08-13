#!/user/bin/env python3
""" app flak """
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """ return the follow message """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    """ run the flask """
    app.run(host='0.0.0.0', port="5000")
