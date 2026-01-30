# pegasus_framework/auth/models/sessions/auth_session_base.py
from sqlalchemy.orm import declarative_mixin, mapped_column, Mapped
from sqlalchemy import String
from datetime import datetime
from sqlalchemy import DateTime

@declarative_mixin
class AuthSessionBase:
    """
    Modelo base abstracto para sesiones "logicas" de usuario.

    - NO define __tablename__
    - NO define claves foráneas concretas
    - NO debe ser usado directamente por Alembic

    Una sesion logica de usuario es que representa un usuario logueado en el sistema y 
    eso implica que puede tener un refresh token de larga duracion y uno o varios access tokens
    relacionados, los access tokens pueden estar revocados o vencidos pero el refresh token no
    eso implica que la sesion logica continua vigente mientras el refresh token siga vigente.
    """    
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="active" # hay que meter esto en un enum y trabajar con ese enum
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    ip_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    user_agent: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    accept_language: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
