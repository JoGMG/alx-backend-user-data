#!/usr/bin/env python3
"""
Basic Authentication System Management.
"""
from api.v1.auth.auth import Auth


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
