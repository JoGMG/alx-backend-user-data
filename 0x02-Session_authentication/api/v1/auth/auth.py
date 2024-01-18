#!/usr/bin/env python3
"""
API Authentication System Management.
"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """
    API Authentication System Manager.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns `True` if `path` requires authentication, else `False`.

        Arguments:
            - `path`: HTTP request path (url) to check.
            - `excluded_paths`: List of paths (url) that do not require
            authentication.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        for x_path in excluded_paths:
            if x_path.endswith('*'):
                end = x_path.split('/')[-1][:-1]
                if end in path:
                    return False
        if not path.endswith('/'):
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns `request` Authorization Header key.

        Arguments:
            - `request`: HTTP request.
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization', None)
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns User instance for a request.

        Arguments:
            - `request`: HTTP request.
        """
        return None

    def session_cookie(self, request=None):
        """
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
