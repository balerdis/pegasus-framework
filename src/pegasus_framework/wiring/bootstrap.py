# pegasus_framework/wiring/bootstrap.py
from pegasus_framework.wiring.providers import provide_uow

from pegasus_framework.business.users.user_service import UserService


def get_user_service() -> UserService:
    return UserService(uow=provide_uow())
