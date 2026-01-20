# pegasus_framework/api/middleware/auth_middleware.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import hashlib
class AuthContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        token = None
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header[7:]

        token_fingerprint = (
            hashlib.sha256(token.encode()).hexdigest()[:16]
            if token else None
        )

        request.state.auth_context = {
            "has_auth_header": bool(auth_header),
            "token_fingerprint": token_fingerprint,
        }

        return await call_next(request)