#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar
from user import Base, User


class DB():
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ method that add new user into the db"""
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ method that found the user row or
            - raise [NoResultFound, InvalidRequest]"""
        try:
            user = self.__session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update the user"""
        try:
            user = self.find_user_by(id=user_id)

            self.__session.query(User).filter_by(id=user_id).update(kwargs)
            self.__session.commit()
            return None
        except ValueError:
            raise
