# pegasus_framework/auth/repositories/sessions/auth_session_repository_base.py
from abc import ABC, abstractmethod
from datetime import datetime
from re import A
from typing import Optional
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext
from pegasus_framework.db.models.auth.sessions.auth_session_base import AuthSessionBase
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
    def get_by_id(
                  self, *, 
                  session_id: int
                  ) -> AuthSessionBase | None:
        raise NotImplementedError


    @abstractmethod
    def revoke_by_id(
                self, 
                id: int, 
                revoked_at: datetime
                ):    
        raise NotImplementedError
    
    @abstractmethod
    def revoke_all_for_user(
                            self, *, 
                            user_id: int, 
                            revoked_at: datetime
                            ):
        raise NotImplementedError
