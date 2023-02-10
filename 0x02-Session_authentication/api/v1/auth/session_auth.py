#!/usr/bin/env python3
""" Session Authorization module
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Basic Authorization Class
    Inheriting from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ instance method to create a session
        """
        if not user_id or type(user_id) is not str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ method to get User id based on session id
        """
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ method to get current user based on cookies
        """
        sess_id = self.session_cookie(request)
        u_id = self.user_id_for_session_id(sess_id)
        return User.get(u_id)

    def destroy_session(self, request=None):
        """ method to destroy session
        """
        sess_id = self.session_cookie(request)
        if not request or not sess_id:
            return False
        u_id = self.user_id_for_session_id(sess_id)
        if not u_id:
            return False
        self.user_id_by_session_id.pop(sess_id)
        return True
