# pegasus_framework/business/users/dto/create.py
from .base import UserBaseDTO
from pydantic import Field

class UserCreateDTO(UserBaseDTO):
    password: str = Field(..., min_length=8, max_length=128)