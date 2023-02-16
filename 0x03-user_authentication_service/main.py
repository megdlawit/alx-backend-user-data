#!/usr/bin/env python3
""" module for integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """ test """
    data = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/users', data=data)
    assert response.status_code == 200, "Registration"


def log_in_wrong_password(email: str, password: str) -> None:
    """ test """
    data = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/sessions', data=data)
    assert response.status_code == 401, "Wrong password"


def profile_unlogged() -> None:
    """ test """
    data = {"session_id": ""}
    response = requests.get('http://localhost:5000/profile', data=data)
    assert response.status_code == 403, "Unlogged"


def log_in(email: str, password: str) -> str:
    """ test """
    data = {"email": email, "password": password}
    response = requests.post('http://localhost:5000/sessions', data=data)
    assert response.status_code == 200, "Login"
    session_id = response.cookies.get("session_id")
    return session_id


def profile_logged(session_id: str) -> None:
    """ test """
    data = {"session_id": session_id}
    response = requests.get('http://localhost:5000/profile', cookies=data)
    assert response.status_code == 200, "Logged in"


def log_out(session_id: str) -> None:
    """ test """
    data = {"session_id": session_id}
    response = requests.delete('http://localhost:5000/sessions', cookies=data)
    assert response.status_code == 200, "Logout"


def reset_password_token(email: str) -> str:
    """ test """
    data = {"email": email}
    response = requests.post('http://localhost:5000/reset_password', data=data)
    assert response.status_code == 200, "Reset password"
    reset_token = response.json().get("reset_token")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put('http://localhost:5000/reset_password', data=data)
    assert response.status_code == 200, "Update Password"


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
