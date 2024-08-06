#!/usr/bin/env python3
""" new class that inherit from Auth class"""
from api.v1.auth.auth import Auth


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
