#!/usr/bin/env python3
""" app flak """

from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """ return the follow message """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ route to register a new user """
    if request.method == "POST":
        try:
            AUTH.register_user(request.form["email"], request.form["password"])
            return jsonify(
                {"email": request.form["email"], "message": "user created"}
                )
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    """ run the flask """
    app.run(host='0.0.0.0', port="5000")
