#!/usr/bin/env python3
"""
Session Expiration Authentication System Management.
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session Expiration Authentication System Manager.
    """
    def __init__(self):
        """
        Initializes SessionExpAuth instance attributes.
        """
        try:
            session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Creates a session ID and returns it.

        Arguments:
            - `user_id`: User Instance ID.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Return user ID on duration expiration.

        Arguments:
            - `session_id`: User Authentication Session ID.
        """
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id, None)
        if session_dictionary is None:
            return None
        user_id = session_dictionary.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = session_dictionary.get('created_at', None)
        if created_at is None:
            return None
        duration = created_at + timedelta(seconds=self.session_duration)
        if duration < datetime.now():
            return None
        return user_id
