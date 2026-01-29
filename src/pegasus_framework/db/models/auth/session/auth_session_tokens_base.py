from sqlalchemy.orm import declarative_mixin, mapped_column, Mapped
from sqlalchemy import String, DateTime, JSON
from datetime import datetime
from typing import Any, Dict

@declarative_mixin
class AuthSessionTokensBase:
    """
    Modelo base abstracto para los tokens de sesiones de usuario.
    pueden ser access tokens o refresh tokens

    - NO define __tablename__
    - NO define claves foráneas concretas
    - NO debe ser usado directamente por Alembic

    """    
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

    token_type: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="access" # hay que meter esto en un enum y trabajar con ese enum
    )    

    # hash del token, no el token, el token plano solo vive en el cliente
    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )

    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    """
        Replaced_by_token: 
        Solo para refresh tokens
        Si un refresh token se usa:
            Se revoca
            Se crea uno nuevo
            Se enlazan    
    """
    replaced_by_token: Mapped[int] = mapped_column(
        nullable=True
    )

    """
        ejemplo de uso de extra_data:
            {
            "ip": "181.10.22.4",
            "user_agent": "Chrome/121",
            "rotation_reason": "refresh",
            "device_id": "abc123"
            }        
    """
    extra_data: Mapped[Dict[str, Any]] = mapped_column(
        "metadata",
        JSON,
        nullable=True
    )