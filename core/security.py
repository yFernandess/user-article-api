from passlib.context import CryptContext


CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Function to check if the password is correct, comparing
    the plain text password entered by the user and the password hash
    that will be saved in the database during account creation.
    """

    return CRYPTO.verify(password, password_hash)


def generate_password_hash(password: str) -> str:
    """
    Function that generates and returns the password hash
    """

    return CRYPTO.hash(password)