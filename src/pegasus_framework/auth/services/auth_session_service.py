# pegasus_framework/auth/services/auth_session_service.py
from datetime import datetime
from hmac import new
from operator import ne
import re
from venv import logger

from pegasus_framework.db.repositories.auth.sessions.auth_session_token_repository_base import AuthSessionTokenRepositoryBase
from pegasus_framework.db.repositories.auth.sessions.auth_session_repository_base import AuthSessionRepositoryBase
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext
from pegasus_framework.core.time.clock import Clock
from pegasus_framework.business.domain.auth.token_type import TokenType
from pegasus_framework.auth.dto.token_pair import TokenPairDTO
from pegasus_framework.auth.exceptions.invalid_token import InvalidTokenError
from pegasus_framework.auth.dto.token import TokenDTO
import logging
logger = logging.getLogger(__name__)
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
        token_jti: str,
        now: datetime | None = None,
        token_type: TokenType = TokenType.ACCESS
    ):
        if now is None:
            now = Clock.now_utc()        
        
        auth_session_token_repo = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_repo = self._uow.repo(AuthSessionRepositoryBase)

        token = auth_session_token_repo.get_valid_by_token_jti(
            token_jti=token_jti,
            now=now,
            token_type=token_type.value
        )

        if token is None:
            return None

        session = auth_session_repo.get_by_id(session_id=token.auth_session_id)

        if session is None or session.revoked_at is not None:
            return None

        return session   



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

    def renew_session(
        self,
        *,
        refresh_token_jti: str,
        new_access_token: TokenDTO,
        new_refresh_token: TokenDTO,
        expected_user_id: int
    ) -> TokenPairDTO:
        now = Clock.now_utc()
        # Obtener el refresh token
        # Verificar el refresh token activo en la DB
        refresh_token = self.check_refresh_token_validity(refresh_token_jti=refresh_token_jti)
        session = self._uow.repo(AuthSessionRepositoryBase).get_by_id(
            session_id=refresh_token.auth_session_id
        )

        if session.user_id != expected_user_id:
            self.revoke_session_by_id(session.id, revoked_at=now)
            raise InvalidTokenError("Refresh token does not belong to user")
        
        # Revocar el refresh token recibido
        self.revoke_token(refresh_token_jti=refresh_token_jti)
        # Emitir nuevo access token
        access_token_new = new_access_token
        # Emitir nuevo refresh token
        refresh_token_new = new_refresh_token
        # persistar los 2 nuevos tokens
        self.save_tokens(
            access_token=access_token_new,
            refresh_token=refresh_token_new,
            auth_session_id=refresh_token.auth_session_id
        )
        # en el refresh viejo : replaced_by_token_id = new_refresh_token.id
        self.update_refresh_token_replaced_by(
            refresh_token_jti=refresh_token.token_jti,
            replaced_by_token_jti=refresh_token_new.token_jti
        )
        #responder con los 2 nuevos tokens y sus fechas de expiración
        return TokenPairDTO(
            access_token=access_token_new.token,
            expires_at=access_token_new.expires_at,
            refresh_token=refresh_token_new.token,
            refresh_token_expires_at=refresh_token_new.expires_at
        )     

    def revoke_token(
        self,
        *,
        refresh_token_jti: str,
        revoked_at: datetime | None = None
    ) -> None:
        if revoked_at is None:
            revoked_at = Clock.now_utc()
        auth_session_token_repository = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_token_repository.revoke_by_token_jti(token_jti=refresh_token_jti, revoked_at=revoked_at)

    def check_refresh_token_validity(
        self,
        *,
        refresh_token_jti: str,
    ) -> None:
        logger.info(f"check_refresh_token_validity: {refresh_token_jti}")
        now = Clock.now_utc()
        auth_session_token_repository = self._uow.repo(AuthSessionTokenRepositoryBase)
        refresh_token = auth_session_token_repository.get_valid_refresh_token(
            token_jti=refresh_token_jti,
            now=now,
        )
        if not refresh_token:
            raise InvalidTokenError("Refresh token invalido")

        if refresh_token.replaced_by_token is not None:
            # token reuse detectado
            self.revoke_session_by_id(refresh_token.auth_session_id, revoked_at=now)
            raise InvalidTokenError("Refresh token reuse detected")     
                
        return refresh_token

    def save_tokens(
        self,
        *,
        access_token: TokenDTO,
        refresh_token: TokenDTO,
        auth_session_id: int,
    ) -> None:
        auth_session_token_repository = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_token_repository.create(
            auth_session_id=auth_session_id,
            token_jti=access_token.token_jti,
            token_type=TokenType.ACCESS.value,
            issued_at=access_token.issued_at,
            expires_at=access_token.expires_at,
        )

        auth_session_token_repository.create(
            auth_session_id=auth_session_id,
            token_jti=refresh_token.token_jti,
            token_type=TokenType.REFRESH.value,
            issued_at=refresh_token.issued_at,
            expires_at=refresh_token.expires_at,
        )

    def update_refresh_token_replaced_by(
        self,
        *,
        refresh_token_jti: str,
        replaced_by_token_jti: str,
    ) -> None:
        auth_session_token_repository = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_token_repository.update_refresh_token_replaced_by(
            refresh_token_jti=refresh_token_jti,
            replaced_by_token_jti=replaced_by_token_jti,
        )

    def revoke_session_by_id(
        self,
        *,
        auth_session_id: int,
        revoked_at: datetime
    ) -> None:
        auth_session_repository = self._uow.repo(AuthSessionRepositoryBase)
        auth_session_repository.revoke_by_id(id=auth_session_id, revoked_at=revoked_at)
        auth_session_token_repository = self._uow.repo(AuthSessionTokenRepositoryBase)
        auth_session_token_repository.revoke_by_auth_session_id(auth_session_id=auth_session_id, revoked_at=revoked_at)