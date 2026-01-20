# pegasus_framework/api/middleware/rate_limit/rate_limit_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import NamedTuple
from .in_memory_rate_limiter import InMemoryRateLimiter

RATE_LIMITS = {
    "token": (1000, 60),  # 1000 req/min
    "ip": (100, 60),      # 100 req/min
}

class RateLimitPolicy(NamedTuple):
    key: str
    limit: int
    window: int

class RateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, limiter: InMemoryRateLimiter):
        super().__init__(app)
        self.limiter = limiter
    async def dispatch(self, request: Request, call_next):
        endpoint_class = self._classify_endpoint(request)
        policy = self._resolve_policy(endpoint_class, request)

        if policy and not self.allow_request(policy):
            raise HTTPException(status_code=429, detail="Too many requests")

        return await call_next(request)

    def _classify_endpoint(self, request: Request) -> str:
        path = request.url.path

        if path == "/api/v1/auth/login":
            return "AUTH_LOGIN"

        if path == "/api/v1/auth/logout":
            return "AUTH_LOGOUT"

        if path.startswith("/api/v1/system"):
            return "INTERNAL"

        return "DEFAULT"

    def _resolve_policy(self, endpoint_class: str, request: Request):
        ctx = getattr(request.state, "auth_context", {})
        ip = request.client.host

        if endpoint_class == "AUTH_LOGIN":
            return RateLimitPolicy(key=f"login:{ip}", limit=5, window=60)

        if ctx.get("token_fingerprint"):
            return RateLimitPolicy(key=f"token:{ctx['token_fingerprint']}", limit=1000, window=60)

        return RateLimitPolicy(key=f"ip:{ip}", limit=100, window=60)

    def allow_request(self, policy: RateLimitPolicy) -> bool:
        # implementación real → Redis / in-memory / etc.
        return self.limiter.allow(policy.key, policy.limit, policy.window)