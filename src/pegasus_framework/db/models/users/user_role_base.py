# pegasus_framework/db/models/users/user_role_base.py
from sqlalchemy.orm import Mapped, mapped_column

class BaseUserRole:
    __abstract__ = True
    user_id: Mapped[int] = mapped_column(
        primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        primary_key=True
    )