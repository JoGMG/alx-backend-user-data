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

    def create_session(self, email: str) -> str:
        """
        Returns the session ID of a user object as a string.

        Argument:
            - `email`: User object email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Finds and returns user object by `session_id`, else None.

        Arguments:
            - `session_id`: User object authentication session id.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """
        Updates user object's `session_id` to None and returns it.

        Arguments:
            - `user_id`: User object id.
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Updates user object's `reset_token` and returns it.

        Arguments:
            - `email`: User object email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates user object's `password` with the new hashed password
        and sets user object's `reset_token` to None.

        Argument:
            - `reset_token`: User object's reset_token.
            - `password`: password to update user object with.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)
        return None
