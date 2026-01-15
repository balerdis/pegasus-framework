# pegasus_framework/auth/models/users/user_base.py

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class BaseUser:
    __abstract__ = True

    # === Identidad ===
    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # === Datos personales ===
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # === Estado ===
    habilited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # === Auditoría ===
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    modificated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # === Contratos de comportamiento ===
    def can_login(self) -> bool:
        return self.habilited and self.deleted_at is None
