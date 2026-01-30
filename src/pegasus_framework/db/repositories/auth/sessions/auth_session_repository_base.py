# pegasus_framework/auth/repositories/sessions/auth_session_repository_base.py
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext

class AuthSessionRepositoryBase(ABC):
    """
    Contrato para la persistencia y gestión de sesiones logicas del usuario.

    Este repositorio define las operaciones mínimas que el sistema
    de autenticación necesita para validar, revocar y crear sesiones.
    """

    @abstractmethod
    def create(
        self,
        *,
        user_id: int,
       context: AuthRequestContext | None = None
    ):
        """
        Persiste una nueva sesión logica para un usuario.

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
        Retorna la sesión válida asociada al access_token_id o None si:

        - no existe
        - está revocada
        - está expirada
        """
        raise NotImplementedError


    @abstractmethod
    def revoke(
        self,
        *,
        access_token_jti: str,
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
        revoked_at: Optional[datetime],
    ) -> int:
        """
        Revoca todas las sesiones activas de un usuario.

        Retorna la cantidad de sesiones revocadas.
        """
        raise NotImplementedError
