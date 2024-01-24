#!/usr/bin/env python3
"""
Auth Module.
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of `password`.

    Arguments:
        - `password`: string password.
    """
    encoded_pword = password.encode()
    hashed_pword = bcrypt.hashpw(encoded_pword, bcrypt.gensalt())
    return hashed_pword


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
