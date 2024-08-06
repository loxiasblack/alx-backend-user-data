#!/usr/bin/env python3
""" new class Auth """
from typing import List, TypeVar
from flask import request
from api.v1.views.users import User


class Auth:
    """ the class auth """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require path method """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith("/"):
            path += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth path method """
        if request is None:
            return None
        if "Authorization" not in request.headers.keys():
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method """
        return None
