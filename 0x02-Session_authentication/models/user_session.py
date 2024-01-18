#!/usr/bin/env python3
"""
Manages the storage of Session ID in DataBase.
"""
from models.base import Base


class UserSession(Base):
    """
    User Session ID Storage Manager.
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes UserSession instance attributes.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
