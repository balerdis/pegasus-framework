from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import uuid

import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError

from pegasus_framework.core.exceptions.domain import InvalidAccessTokenError



class JwtTokenService:
    """
    Servicio técnico para generación y validación de JWT.

    - Stateless
    - Sin acceso a base de datos
    - No conoce User ni SessionRepository
    """

    def __init__(
        self,
        *,
        secret_key: str,
        algorithm: str = "HS256",
        issuer: str | None = None,
        audience: str | None = None,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._issuer = issuer
        self._audience = audience

    def generate_token(
        self,
        *,
        subject: str,
        expires_delta: timedelta,
        additional_claims: Dict[str, Any] | None = None,
        now: datetime | None = None,
    ) -> Dict[str, Any]:
        """
        Genera un JWT y retorna:
        - el token serializado
        - el token_id (jti)
        - expires_at
        """
        if now is None:
            now = datetime.now(timezone.utc)

        expires_at = now + expires_delta
        token_id = str(uuid.uuid4())

        payload: Dict[str, Any] = {
            "sub": subject,
            "jti": token_id,
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
        }

        if self._issuer:
            payload["iss"] = self._issuer

        if self._audience:
            payload["aud"] = self._audience

        if additional_claims:
            payload.update(additional_claims)

        token = jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

        return {
            "access_token": token,
            "token_id": token_id,
            "expires_at": expires_at,
        }

    def decode_and_validate(
        self,
        *,
        token: str,
    ) -> Dict[str, Any]:
        """
        Decodifica y valida un JWT.

        Lanza excepción si:
        - firma inválida
        - expirado
        - issuer / audience inválidos
        """
        options = {
            "require": ["exp", "iat", "jti", "sub"],
        }
        try:
            decoded = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
                issuer=self._issuer,
                audience=self._audience,
                options=options,
            )

        except ExpiredSignatureError:
            # Específico para tokens cuya fecha 'exp' ya pasó
            raise InvalidAccessTokenError("Token expirado")

        except PyJWTError:
            raise InvalidAccessTokenError()      

        return decoded

    @staticmethod
    def extract_token_id(
        *,
        decoded_payload: Dict[str, Any],
    ) -> str:
        """
        Extrae el token_id (jti) de un payload ya validado.
        """
        return decoded_payload["jti"]
