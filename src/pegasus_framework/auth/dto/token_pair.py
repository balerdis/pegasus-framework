# pegasus_framework/auth/dto/token_pair.py
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TokenPairDTO:
    access_token: str
    expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime
    token_type: str = "bearer"