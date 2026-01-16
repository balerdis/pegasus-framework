# pegasus_framework/auth/models/sessions/user_session_base.py
from datetime import datetime
from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, declarative_mixin


@declarative_mixin
class UserSessionBase:
    """
    Modelo base abstracto para sesiones de usuario.

    - NO define __tablename__
    - NO define claves foráneas concretas
    - NO debe ser usado directamente por Alembic
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    token_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
        index=True,
        doc="Identificador único del token (jti o equivalente)"
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indica si la sesión/token fue revocado"
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="Momento en que la sesión/token expira"
    )
