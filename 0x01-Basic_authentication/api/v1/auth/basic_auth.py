#!/usr/bin/env python3
"""
Basic Authentication System Management.
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication System Manager.
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of `authorization header` for a
        Basic Authentication.

        Arguments:
            - `authorization_header`: HTTP request authorization
            header encoded in base64 format.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of `base64_authorization_header`.

        Arguments:
            - `base64_authorization_header`: HTTP request authorization
            header encoded in base64 format.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from
        `decoded_base64_authorization_header`.

        Arguments:
            - `decoded_base64_authorization_header`: Decoded HTTP
            request authorization header.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email = decoded_base64_authorization_header.split(':')[0]
        user_pwd = decoded_base64_authorization_header[len(user_email) + 1:]
        return user_email, user_pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.

        Arguments:
            - `user_email`: User email.
            - `user_pwd`: User password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads `Auth.current_user`, returns User instance for a request.

        Arguments:
            - `request`: HTTP request.
        """
        auth_header = self.authorization_header(request)
        auth_key = self.extract_base64_authorization_header(auth_header)
        decoded_auth_key = self.decode_base64_authorization_header(auth_key)
        user_email, user_pwd = self.extract_user_credentials(decoded_auth_key)
        return self.user_object_from_credentials(user_email, user_pwd)
