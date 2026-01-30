# pegasus_framework/auth/repositories/sessions/auth_session_token_repository.py
from abc import ABC, abstractmethod
from datetime import datetime
import enum
from typing import Optional


class TokenType(enum.Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"
class AuthSessionTokenRepository(ABC):

    def __init__(self):
        super().__init__()
        self.TokenType: enum = TokenType
    @abstractmethod
    def create(self, 
               *,
               token_id: str,
               expires_at: datetime,
               token_type: str
               ):
        raise NotImplementedError
    
    @abstractmethod
    def revoke(self, 
               *,
               token_id: str,
               revoked_at: Optional[datetime] = None
               ):
        raise NotImplementedError
    
    @abstractmethod
    def get_valid_by_token_id(self, 
                              *,
                              token_id: str,
                              now: datetime
                              ):
        raise NotImplementedError
    
    @abstractmethod
    def get_valid_by_refresh_token_id(self, 
                                     *,
                                     token_id: str,
                                     now: datetime
                                     ):
        raise NotImplementedError
    
    @abstractmethod
    def get_valid_by_access_token_id(self, 
                                    *,
                                    token_id: str,
                                    now: datetime
                                    ):
        raise NotImplementedError
    
    
    @abstractmethod
    def get_all_by_user_id(self, 
                           *,
                           user_id: int
                           ):
        raise NotImplementedError
    
   
    @abstractmethod
    def get_all_by_token_type_and_user_id(self, 
                                          *,
                                          token_type: str,
                                          user_id: int
                                          ):
        raise NotImplementedError