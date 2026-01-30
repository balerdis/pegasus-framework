from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TokenDTO:
    token_jti: str
    token: str
    expires_at: datetime
    issued_at: datetime
