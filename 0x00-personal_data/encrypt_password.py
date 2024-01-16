#!/usr/bin/env python3
"""
Encrypting and validating passwords for safe storage.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password.

    Arguments:
    - `password`: Password to be hashed.
    """
    b_password = password.encode()
    hashed = bcrypt.hashpw(b_password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Returns `True` if the provided `password` matches the
    `hashed password`, else `False`.

    Arguments:
    - `hashed_password`: Hashed password.
    - `password`: Normal password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
