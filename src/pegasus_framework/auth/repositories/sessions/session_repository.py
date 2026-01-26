# pegasus_framework/auth/repositories/sessions/session_repository.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class SessionRepository(ABC):
    """
    Contrato para la persistencia y gestión de sesiones de usuario.

    Este repositorio define las operaciones mínimas que el sistema
    de autenticación necesita para validar, revocar y crear sesiones.
    """

    @abstractmethod
    def create(
        self,
        *,
        user_id: int,
        token_id: str,
        expires_at: datetime,
    ):
        """
        Persiste una nueva sesión para un usuario.

        Retorna la sesión creada (tipo concreto definido por la app).
        """
        raise NotImplementedError

    @abstractmethod
    def get_valid_by_token_id(
        self,
        *,
        token_id: str,
        now: datetime,
    ):
        """
        Retorna la sesión válida asociada al token_id o None si:

        - no existe
        - está revocada
        - está expirada
        """
        raise NotImplementedError

    @abstractmethod
    def revoke(
        self,
        *,
        token_id: str,
        revoked_at: Optional[datetime] = None,
    ) -> None:
        """
        Revoca una sesión existente.

        La revocación debe ser idempotente.
        """
        raise NotImplementedError

    @abstractmethod
    def revoke_all_for_user(
        self,
        *,
        user_id: int,
    ) -> int:
        """
        Revoca todas las sesiones activas de un usuario.

        Retorna la cantidad de sesiones revocadas.
        """
        raise NotImplementedError
