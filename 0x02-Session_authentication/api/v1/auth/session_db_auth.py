#!/usr/bin/env python3
"""
Database Session Authentication Management.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Database Session Authentication Manager.
    """
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession and
        returns the Session ID.

        Arguments:
            - `user_id`: User instance id.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        attributes = {
            'user_id': user_id,
            'session_id': session_id
        }
        user_session = UserSession(**attributes)
        user_session.save()
        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession in the
        database based on `session_id`.

        Arguments:
            - `session_id`: User Authentication Session ID.
        """
        if session_id is None:
            return None
        duration = super().user_id_for_session_id(session_id)
        if duration is None:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID from the
        request cookie.

        Arguments:
            - `request`: HTTP request to get cookie.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        del self.user_id_by_session_id[session_id]
        return True
