# pegasus_framework/db/models/auth/roles_permission/rol_permission_base.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
class BaseRolePermission:
    __abstract__ = True

    role_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    permission_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    
