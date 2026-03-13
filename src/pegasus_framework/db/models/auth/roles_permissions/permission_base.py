# pegasus_framework/db/models/auth/roles_permission/permission_base.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class BasePermission:
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)