#!/usr/bin/env python3
"""
Session Authentication System Management.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Authentication System Manager.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a session ID for a `user_id` returns it.

        Arguments:
            - `user_id`: User instance ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the user ID for a `session_id`.

        Arguments:
            - `session_id`: A random UUID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)