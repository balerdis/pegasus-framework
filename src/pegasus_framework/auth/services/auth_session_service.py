# pegasus_framework/auth/services/auth_session_service.py
from datetime import datetime

from pegasus_framework.db.repositories.auth.sessions.auth_session_token_repository_base import AuthSessionTokenRepositoryBase
from pegasus_framework.db.repositories.auth.sessions.auth_session_repository_base import AuthSessionRepositoryBase
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext
from pegasus_framework.core.time.clock import Clock
from pegasus_framework.business.domain.auth.token_type import TokenType
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
        access_token_jti: str,
        access_token_expires_at: datetime,
        access_token_issued_at: datetime,
        refresh_token_jti: str,
        refresh_token_expires_at: datetime,
        refresh_token_issued_at: datetime,
        context: AuthRequestContext | None = None
    ):
        """El metodo de authSessionService crea una session, siempre que se lo pidan

        Args:
            user_id (int): id del usuario que requiere una session
            access_token_id (str): id del access_token generado para esta session
            access_expires_at (_type_): fecha de expiración del access_token
            refresh_token_id (str): id del refresh_token generado para esta session
            refresh_expires_at (_type_): fecha de expiración del refresh_token

        Returns:
            _type_: None
        """
        # con el repositorio de AuthSessionRepository, crea un registro en la tabla auth_sessions
        # el id de la auth_session, con el AuthSessionTokensRepository, crea un registro en la tabla auth_session_tokens
        # para el access_token y un registro para el refresh_token (indica el tipo de token al momento de persistir con 
        # el enum a definir)
        repo_auth_session = self._uow.repo(AuthSessionRepositoryBase)

        auth_session = repo_auth_session.create(
            last_activity_at = Clock.now_utc(), 
            expires_at= refresh_token_expires_at, 
            user_id=user_id, 
            context=context
            )

        repo_auth_session_token = self._uow.repo(AuthSessionTokenRepositoryBase)
        repo_auth_session_token.create(
            auth_session_id=auth_session.id,
            token_jti=access_token_jti,
            token_type=TokenType.ACCESS.value,
            issued_at=access_token_issued_at,
            expires_at=access_token_expires_at,
        )

        repo_auth_session_token.create(
            auth_session_id=auth_session.id,
            token_jti=refresh_token_jti,
            token_type=TokenType.REFRESH.value,
            issued_at=refresh_token_issued_at,
            expires_at=refresh_token_expires_at,
        )



        return auth_session

    def get_valid_session(
        self,
        *,
        token_id: str,
        now: datetime = Clock.now_utc(),
    ):
        repo = self._uow.repo(AuthSessionRepositoryBase)
        return repo.get_valid_by_access_token_id(
            token_id=token_id,
            now=now,
        )


    def revoke_session(
        self,
        *,
        access_token_jti: str,
    ) -> None:
        now = Clock.now_utc()

        auth_session_token_repo = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_repo = self._uow.repo(AuthSessionRepositoryBase)

        token = auth_session_token_repo.get_valid_access_token(
            token_jti=access_token_jti,
            now=now,
        )

        if token is None:
            return  # logout idempotente

        session = auth_session_repo.get_by_id(session_id=token.auth_session_id)

        if session is None or session.revoked_at is not None:
            return

        auth_session_repo.revoke_by_id(
            id=session.id,
            revoked_at=now,
        )

        auth_session_token_repo.revoke_by_auth_session_id(
            auth_session_id=session.id,
            revoked_at=now,
        )        



