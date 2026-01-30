# pegasus_framework/auth/context/auth_request_context.py
from dataclasses import dataclass
from ipaddress import ip_address
from typing import Optional


@dataclass(frozen=True)
class AuthRequestContext:
    ip_address: ip_address
    user_agent: Optional[str]
    accept_language: Optional[str]