from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from collections.abc import Awaitable, Callable
import json, logging

from app.api.v1.schemas.generic import TokenInfo

from pegasus_framework.auth.api.token_handler import TokenHandler


logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, excluded_paths: list[str], protected_paths: list[str]):
        super().__init__(app)

        self.token_handler = TokenHandler()

        self.excluded_paths = excluded_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/health",
            "/favicon.ico"
        ]
        self.protected_paths = protected_paths or [
            "/api/v1/ask",
            "/api/v1/users"
        ]
        logger.info(f"AuthMiddleware inicializado con {len(self.excluded_paths)} rutas excluidas y {len(self.protected_paths)} rutas protegidas")
    

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path

        if self._is_excluded_path(path):
            logger.debug(f"Ruta excluida de autenticación: {request.url.path}")
            return await call_next(request)
        
        user = None
        try:
            user = self._authenticate_request(request)
        except HTTPException as e:
            return self._create_unauthorized_response(e.detail)
        except Exception as ex:
            return self._create_unauthorized_response(f"Error interno en la autenticación: {ex}")

        if self._is_protected_path(path) and not user:
            logger.warning(f"Acceso denegado a ruta protegida: {request.url.path}")
            return self._create_unauthorized_response(
                "Acceso denegado a ruta protegida" 
            )

        # Log del estado de autenticación
        if user:
            logger.debug(f"Usuario autenticadopara ruta: {request.url.path}")
        else:
            logger.debug(f"Acceso sin autenticación a ruta: {request.url.path}")
        
        # Continuar con el request
        return await call_next(request)
    
    def _authenticate_request(
        self,
        request: Request,
    ) -> TokenInfo | None:
        token, client_key = self._extract_token(request)

        if not token or not client_key:
            return None

        if not self._is_token_valid(token, client_key):
            return None

        payload = self.token_handler.decode_token(token, client_key)

        logger.info(f"Token decodificado: {payload}")

        request.state.user_id = payload["usuario_id"]
        request.state.username = payload["usuario_email"]
        request.state.payload = payload

        return payload


    def _is_excluded_path(self, path: str) -> bool:
        return any(path.startswith(excluded) for excluded in self.excluded_paths)

    def _is_protected_path(self, path: str) -> bool:
        return any(path.startswith(protected) for protected in self.protected_paths)
    
    def _extract_token(
        self,
        request: Request,
    ) -> tuple[str | None, str | None]:
        auth_header = request.headers.get("X-Authorization")
        auth_header_json = json.loads(auth_header) if auth_header else {}

        return auth_header_json.get("token"), auth_header_json.get("clientKey")

    def _is_token_valid(
        self,
        token: str,
        client_key: str,
    ) -> bool:
        return self.token_handler.verify_token(token, client_key)

    def _create_unauthorized_response(self, message: str) -> Response:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": message,
                "type": "authentication_error"
            }, 
            headers={"WWW-Authenticate": "X-Authorization"}
        )
    
def verify_active_user() -> bool:
    return True
