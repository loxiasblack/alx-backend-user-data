#!/usr/bin/env python3
""" new class that inherit from Auth class"""
from api.v1.auth.auth import Auth
from base64 import b64decode


class BasicAuth(Auth):
    """ new basic class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base 64 """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """ decode base 64 """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = b64decode(base64_authorization_header)
        except Exception:
            return None
        return decode.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> (str, str):
        """ extract user credentials method """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header.split(":")[-1]
        return (user, password)
