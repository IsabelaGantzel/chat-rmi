import passlib
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password):
    return crypt_context.hash(password)


def check_password(password, hashed_password):
    try:
        return crypt_context.verify(password, hashed_password)
    except passlib.exc.UnknownHashError:
        return False
