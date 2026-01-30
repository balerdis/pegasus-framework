from pegasus_framework.auth.context.auth_request_context import AuthRequestContext
from fastapi import Request

def build_auth_request_context(request: Request) -> AuthRequestContext:


    headers = request.headers


    ip = (
        headers.get('cf-connecting-ip')
        or headers.get('x-forwarded-for', "").split(",")[0].strip()
        or headers.client.host
        if request.client else None
    )

    return AuthRequestContext(
        ip_address=ip,
        user_agent=headers.get("User-Agent"),
        accept_language=headers.get("Accept-Language"),
    )
