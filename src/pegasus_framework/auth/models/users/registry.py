# pegasus_framework/auth/models/users/registry.py
from typing import Type
from pegasus_framework.auth.models.users.user_base import BaseUser

_user_model: Type[BaseUser] | None = None


def register_user_model(model: Type[BaseUser]) -> None:
    global _user_model
    _user_model = model


def get_user_model() -> Type[BaseUser]:
    if _user_model is None:
        raise RuntimeError(
            "User model not registered. "
            "The application must call register_user_model()."
        )
    return _user_model
