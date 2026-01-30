# pegasus_framework/auth/services/auth_service.py

from datetime import datetime, timezone

from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService
from pegasus_framework.auth.security.tokens.jwt_token_service import JwtTokenService
from pegasus_framework.auth.security.hash_password import PasswordHasher

from pegasus_framework.core.exceptions.domain import InvalidCredentialsError, InvalidAuthSessionError
from pegasus_framework.auth.services.auth_session_service import AuthSessionService
from pegasus_framework.auth.dto.token_pair import TokenPairDTO

from pegasus_framework.db.repositories.user_repository import UserRepository
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext

class  AuthService(SqlAlchemyService):
    """
    Servicio de aplicación para autenticación.

    - Orquesta JWT + sesiones persistentes
    - Usa Unit of Work
    - No conoce HTTP ni FastAPI
    """

    def __init__(
        self,
        *,
        token_service: JwtTokenService,
        password_hasher: PasswordHasher,
    ):
        super().__init__()
        self._token_service = token_service
        self._password_hasher = password_hasher

    def login(
        self,
        *,
        identifier: str,
        password: str,
        context: AuthRequestContext | None = None,
        now: datetime | None = None,
    ) -> TokenPairDTO:
        """
        Autentica un usuario y retorna un access token JWT.
        El servicio promulga multisession por usuario que permite loggearse en distintos dispositivos
        """
        if now is None:
            now = datetime.now(timezone.utc)

        with self._uow() as uow:
            users_repo = uow.repo(UserRepository)

            user = users_repo.get_by_email(identifier)

            if not user:
                self._password_hasher.verify(password, self._password_hasher.hash("dummy"))
                raise InvalidCredentialsError()
            
            # seguridad para evitar ataque de fuerza bruta
            hashed_password = (
                user.password
                if user
                else self._password_hasher.hash("dummy-password")
            )            

            if not self._password_hasher.verify(password, hashed_password):
                raise InvalidCredentialsError()

            access_token_data = self._token_service.generate_access_token(
                subject=str(user.id)
            )

            refresh_token_data = self._token_service.generate_refresh_token(
                subject=str(user.id)
            )

            # Creamos una session logica del usuario
            AuthSessionService(uow).create_session(
                user_id=user.id,
                access_token_id=access_token_data.token_id,
                access_token_expires_at=access_token_data.expires_at,
                refresh_token_id=refresh_token_data.token_id,
                refresh_token_expires_at=refresh_token_data.expires_at,
                context=context
            )


            # Importante: siempre el service debe commitear su UoW
            uow.commit()
            return TokenPairDTO(
                access_token=access_token_data.token,
                expires_at=access_token_data.expires_at,
                refresh_token=refresh_token_data.token,
                refresh_token_expires_at=refresh_token_data.expires_at
            )


    def logout(
        self,
        *,
        token: str,
    ) -> None:
        """
        Revoca la sesión asociada al token JWT.
        """
        decoded = self._token_service.decode_and_validate(token=token)
        refresh_token_id = self._token_service.extract_token_id(
            decoded_payload=decoded
        )

        with self._uow() as uow:
            AuthSessionService(uow).revoke_session(
                refresh_token_id=refresh_token_id
            )
            uow.commit()

    def authenticate(self, *, token: str, now: datetime | None = None) -> int:
        """
        Autentica una identidad a partir de un access token.

        - Valida JWT
        - Valida sesión
        - Retorna user_id
        """
        if now is None:
            now = datetime.now(timezone.utc)

        decoded = self._token_service.decode_and_validate(token=token)
        token_id = self._token_service.extract_token_id(
            decoded_payload=decoded
        )

        with self._uow() as uow:
            session = AuthSessionService(uow).get_valid_session(
                token_id=token_id,
                now=now,
            )

        if session is None:
            raise InvalidAuthSessionError()

        # El subject del JWT define la identidad
        return int(decoded["sub"])
