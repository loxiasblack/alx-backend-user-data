#!/usr/bin/env python3
""" new session Auth """
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """ the class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ create a session method """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ create user_id for session_id method """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ current user method"""
        session_id = self.session_cookie(request)
        user_id_for_session = self.user_id_for_session_id(session_id)
        current_user = User.get(user_id_for_session)
        return current_user

    def destroy_session(self, request=None) -> bool:
        """ delete the user session """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_by_session_id = self.user_id_for_session_id(session_id)
        if not user_by_session_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
