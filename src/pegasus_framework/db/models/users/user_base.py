# pegasus_framework/auth/models/users/user_base.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr


class BaseUser:
    __abstract__ = True

    # === Identidad ===
    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(primary_key=True)    

    @declared_attr
    def email(cls) -> Mapped[str]:
        return mapped_column(String(255), unique=True, nullable=False)

    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # === Datos personales ===
    name: Mapped[str | None] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # === Contratos de comportamiento ===
    def can_login(self) -> bool:
        return self.habilited and self.deleted_at is None
