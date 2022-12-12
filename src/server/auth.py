from enum import IntEnum
import sqlite3

from .db import register_user, get_user
import libraries.crypt as crypt


class AuthError(IntEnum):
    UserNotFound = 0
    UserAlreadyExists = 1
    InvalidPassword = 2


def signin(username: str, password: str):
    user = get_user(username)
    if user is None:
        return (None, AuthError.UserNotFound)
    if not crypt.check_password(password, user.password):
        return (None, AuthError.InvalidPassword)
    return (user, None)


def signup(username: str, password: str):
    try:
        hashed_password = crypt.hash_password(password)
        new_user = register_user(username, hashed_password)
        return (new_user, None)
    except sqlite3.IntegrityError as e:
        message = str(e)
        if message == "UNIQUE constraint failed: usuarios.acesso":
            return (None, AuthError.UserAlreadyExists)
        raise e

