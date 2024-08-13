#!/usr/bin/env python3
""" new method add to auth.py """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash the password with bccrypt"""

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register new user into the db """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_password = _hash_password(password)
            user = self._db.add_user(email, hash_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ check if it is a valid login """
        try:
            user = self._db.find_user_by(email=email)
            pwd = password.encode("utf-8")
            if not bcrypt.checkpw(pwd, user.hashed_password):
                return False
            return True
        except NoResultFound:
            return False
