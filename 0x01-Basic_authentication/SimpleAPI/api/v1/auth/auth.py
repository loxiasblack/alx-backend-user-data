#!/usr/bin/env python3
""""""
from typing import List, TypeVar
from flask import request
from api.v1.views.users import User



class Auth:
    """"""
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
