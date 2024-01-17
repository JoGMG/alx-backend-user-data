#!/usr/bin/env python3
"""
API Authentication System Management.
"""
from typing import List, TypeVar
from flask import request


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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns `request` Authorization Header key.

        Arguments:
            - `request`: HTTP request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns User instance for a request.

        Arguments:
            - `request`: HTTP request.
        """
        return None
