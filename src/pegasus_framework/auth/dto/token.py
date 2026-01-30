from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TokenDTO:
    token_id: str
    token: str
    expires_at: datetime
