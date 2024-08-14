#!/usr/bin/env python3
""" app flak """

from flask import Flask, jsonify, request, abort, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ new login route for the session """
    if request.method == "POST":

        # login with auth.valid_login method
        login = AUTH.valid_login(
            request.form["email"], request.form["password"]
            )

        # if it's false abort with 401 status
        if not login:
            abort(401)

        # create new session with auth.create_session
        new_session = AUTH.create_session(request.form["email"])
        json_response = jsonify(
            {"email": request.form["email"], "message": "logged in"}
            )
        # set cookie with session_id
        json_response.set_cookie(new_session)
        return json_response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ logout and delete the session_id """
    # Correctly retrieve the session_id from the cookies
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    # Try to find the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    # Destroy the session and redirect to the homepage
    AUTH.destroy_session(user.id)
    # redirect to the root
    return redirect(url_for("/"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ return the profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": f"{user.email}"}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ reset a password of token """
    # check if request is POST
    if request.method == "POST":
        try:
            # get token rest and check if the email is already register
            token = AUTH.get_reset_password_token(email=request.form["email"])
        except ValueError:
            # abort if not 403 forbidden
            abort(403)
        return jsonify({"email": request.form["email"], "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ update the password """
    # check if the request is PUT
    if request.method == "PUT":
        try:
            # update the password from the form
            AUTH.update_password(
                request.form["reset_token"], request.form["new_password"]
                )
        except ValueError:
            # if the reset_token is invalid abort
            abort(403)
        # return the message showing that the pass has been updated
        return jsonify(
            {"email": request.form["email"], "message": "Password updated"}
            ), 200


if __name__ == "__main__":
    """ run the flask """
    app.run(host='0.0.0.0', port="5000")
