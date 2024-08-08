#!/usr/bin/env python3
""" new view to the session auth"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def session_auth() -> str:
    """ a view to the session """

    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        name_user = user[0].to_json()
        user_id = name_user["id"]
        session_id = auth.create_session(user_id)
        to_json_user = jsonify(user[0].to_json())
        to_json_user.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return to_json_user


@app_views.route('auth_session/logout', methods=["DELETE"],
                 strict_slashes=False)
def logout_from_session() -> str:
    """ new route to the logout """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if not destroy_session:
        abort(404)
    return jsonify({}), 200
