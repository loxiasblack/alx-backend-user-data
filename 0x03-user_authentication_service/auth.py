#!/usr/bin/env python3
""" new method add to auth.py """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """hash the password with bccrypt"""

    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash


def _generate_uuid() -> str:
    """generate uuid"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """ find the user and create a session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ get user from he's session """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroy the current session of the given user"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except InvalidRequestError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ get reset password token """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ update the password """
        try:
            # find the user by the reset token
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # raise value error if not exist
            raise ValueError
        # hash the password
        hashed_pwd = _hash_password(password)
        # update the attribute hased_password and reset_token
        self._db.update_user(
            user.id, hashed_password=hashed_pwd, reset_token=None
            )
