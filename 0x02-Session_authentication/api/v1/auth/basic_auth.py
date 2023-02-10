#!/usr/bin/env python3
""" Basic Authorization module
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from flask import request
from models.user import User


class BasicAuth(Auth):
    """ Basic Authorization Class
    Inheriting from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ method to find base64 string in header
        """
        if not authorization_header or type(authorization_header) is not str:
            return None
        lst = authorization_header.split(" ")
        if lst[0] == 'Basic':
            lst.pop(0)
            return ' '.join(lst)
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ method to decode str by base64
        """
        bah = base64_authorization_header
        if not bah or type(bah) is not str:
            return None
        try:
            bah = base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            bah = None
        return bah

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ method to extract user email and password
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        lst = decoded_base64_authorization_header.split(':')
        if len(lst) < 2:
            return (None, None)
        else:
            email = lst[0]
            lst.pop(0)
            passwd = ':'.join(lst)
        return (email, passwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Method to find and return User instance
            based on email and password
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        u = User()
        lst_usr = u.search({'email': user_email})
        if not lst_usr:
            return None
        for usr in lst_usr:
            if usr.is_valid_password(user_pwd):
                return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ method to authorize request and return user
        """
        if not request:
            return None
        hdr = request.headers['Authorization']
        authorization = self.extract_base64_authorization_header(hdr)
        decoded = self.decode_base64_authorization_header(authorization)
        user_email, user_pwd = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(user_email, user_pwd)
