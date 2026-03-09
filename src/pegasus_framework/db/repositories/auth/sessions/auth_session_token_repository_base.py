# pegasus_framework/auth/repositories/sessions/auth_session_token_repository_base.py
from abc import ABC, abstractmethod
from datetime import datetime
import enum
from typing import Optional
from pegasus_framework.business.domain.auth.token_type import TokenType
from pegasus_framework.db.models.auth.sessions.auth_session_tokens_base import AuthSessionTokensBase

class TokenType(enum.Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"
class AuthSessionTokenRepositoryBase(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TokenType = TokenType
    @abstractmethod
    def create(self, 
               *,
               token_jti: str,
               expires_at: datetime,
               token_type: str
               ):
        raise NotImplementedError
    
    @abstractmethod
    def revoke_by_auth_session_id(self, *, 
                                  auth_session_id: int, 
                                  revoked_at: datetime
                                  ):
        raise NotImplementedError
    
    @abstractmethod
    def get_valid_access_token(
        self,
        *,
        token_jti: str,
        now: datetime,
    ) -> AuthSessionTokensBase | None:
        raise NotImplementedError
    @abstractmethod
    def get_valid_refresh_token(
        self,
        *,
        token_jti: str,
        now: datetime,
    ) -> AuthSessionTokensBase | None:
        raise NotImplementedError
    
    @abstractmethod
    def update_refresh_token_replaced_by(
        self,
        *,
        refresh_token_jti: str,
        replaced_by_token_id: str,
    ) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_valid_by_token_jti(
        self,
        *,
        token_jti: str,
        now: datetime,
        token_type: str,
    ) -> AuthSessionTokensBase | None:
        raise NotImplementedError
    
