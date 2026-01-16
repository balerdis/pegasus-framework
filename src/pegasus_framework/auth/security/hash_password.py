# pegasus_framework/auth/security/hash_password.py

from passlib.context import CryptContext


class PasswordHasher:
    """
    Servicio técnico de hashing de passwords.
    Framework-level.
    """

    def __init__(self):
        self._pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(password, hashed_password)
