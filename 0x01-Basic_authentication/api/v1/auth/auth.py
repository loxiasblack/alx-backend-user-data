#!/usr/bin/env python3
""" new class Auth """
from typing import List, TypeVar
from flask import request
from api.v1.views.users import User


class Auth:
    """ the class auth """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require path method """
        return False

    def authorization_header(self, request=None) -> str:
        """ auth path method """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user method """
        return None
