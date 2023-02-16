#!/usr/bin/env python3
""" module for auth
"""
import typing
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """ method to generate a hashed password
        from a given string
    """
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode(), salt)
    return password


def _generate_uuid() -> str:
    """method to generate id
    """
    id = uuid.uuid4()
    return str(id)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method to register User
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr

    def valid_login(self, email: str, password: str) -> bool:
        """ method to check if a login is valid
        """
        try:
            usr = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), usr.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> str:
        """ method to create a session for user
        """
        try:
            usr = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(usr.id, session_id=sess_id)
            return sess_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str
                                 ) -> typing.Union[User, None]:
        """ method to find user by session id
        """
        if not session_id:
            return None
        try:
            usr = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        else:
            return usr

    def destroy_session(self, user_id: int) -> None:
        """ method to destroy a session of user
        """
        try:
            usr = self._db.find_user_by(id=user_id)
            self._db.update_user(usr.id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """ method that updates reset token field of user
        """
        try:
            usr = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        else:
            id = _generate_uuid()
            usr.reset_token = id
            return id

    def update_password(self, reset_token: str, password: str) -> None:
        """ method to update user password
        """
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        else:
            hashed = _hash_password(password)
            self._db.update_user(usr.id, hashed_password=hashed,
                                 reset_token=None)
