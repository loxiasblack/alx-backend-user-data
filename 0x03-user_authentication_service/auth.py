#!/usr/bin/env python3
"""new method add to auth.py"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash the password with bccrypt"""

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash
