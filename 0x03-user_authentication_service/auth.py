#!/usr/bin/env python3
"""
Auth Module.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of `password`.

    Arguments:
        - `password`: string password.
    """
    encoded_pword = password.encode()
    hashed_pword = bcrypt.hashpw(encoded_pword, bcrypt.gensalt())
    return hashed_pword
