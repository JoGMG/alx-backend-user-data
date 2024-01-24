#!/usr/bin/env python3
"""
Auth Module.
"""
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of `password`.

    Arguments:
        - `password`: string password.
    """
    encoded_pword = password.encode()
    hashed_pword = bcrypt.hashpw(encoded_pword, bcrypt.gensalt())
    return hashed_pword

def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Saves user object to DB and returns it if it exists.

        Arguments:
            - `email`: User object email.
            - `password`: User object password.
        """
        try:
            self._db.find_user_by(email=email)
        except Exception:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Locates user object by email, validates password if it
        exists and returns `True`.

        Arguments:
            - `email`: User object email.
            - `password`: User object password.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)
