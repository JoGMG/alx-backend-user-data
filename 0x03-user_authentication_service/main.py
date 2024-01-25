#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Integration test for registering user object.

    Arguments:
        - `email`: User object email.
        - `password`: User object password.
    """
    url = "http://127.0.0.1:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.status_code == 400
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Integration test for user login with wrong password.

    Arguments:
        - `email`: User object email.
        - `password`: User object password.
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Integration test for user login.

    Arguments:
        - `email`: User object email.
        - `password`: User object password.
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data)
    if response.status_code == 200:
        assert response.json() == {"email": email, "message": "logged in"}
    else:
        assert response.status_code == 401
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    Integration test for user profile when not logged in.
    """
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Integration test for user profile when logged in.

    Arguments:
        - `session_id`: request cookies session id.
    """
    url = "http://127.0.0.1:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Integration test for user logout.

    Arguments:
        - `session_id`: request cookies session id.
    """
    url = "http://127.0.0.1:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    if response.status_code == 200:
        assert response.url == "http://127.0.0.1:5000/"
    else:
        assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """
    Integration test for user reset_password_token.

    Arguments:
        - `email`: User object email.
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data)
    if response.status_code == 200:
        return response.json()["reset_token"]
    else:
        assert response.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Integration test for user password update.

    Arguments:
        - `email`: User object email.
        - `reset_token`: User object reset token.
        - `new_password`: password to update User object with.
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data)
    if response.status_code == 200:
        assert response.json() == {
            "email": email,
            "message": "Password updated"
        }
    else:
        assert response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
