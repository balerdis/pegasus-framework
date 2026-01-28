# pegasus_framework/auth/services/auth_session_service.py
from datetime import datetime

from pegasus_framework.db.repositories.auth.sessions.session_repository import SessionRepository
from pegasus_framework.db.repositories.auth.sessions.session_repository import (
    SessionRepository,
)

class AuthSessionService:
    """
    Servicio de dominio técnico para la gestión de sesiones de autenticación.

    - Usa Unit of Work
    - No conoce HTTP
    - No conoce JWT
    - Orquesta reglas sobre sesiones persistentes
    """    
    def __init__(self, uow):
        self._uow = uow

    def create_session(
        self,
        *,
        user_id: int,
        token_id: str,
        expires_at,
    ):
        # SessionRepository es en realidad SqlAlchemySessionRepository
        repo = self._uow.repo(SessionRepository)
        return repo.create(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
        )

    def get_valid_session(
        self,
        *,
        token_id: str,
        now: datetime,
    ):
        repo = self._uow.repo(SessionRepository)
        return repo.get_valid_by_token_id(
            token_id=token_id,
            now=now,
        )


    def revoke_session(
        self,
        *,
        token_id: str,
    ) -> None:
        repo = self._uow.repo(SessionRepository)
        repo.revoke(token_id=token_id)

    def revoke_all_sessions_for_user(
        self,
        *,
        user_id: int,
    ) -> int:
        repo = self._uow.repo(SessionRepository)
        return repo.revoke_all_for_user(user_id=user_id)
