
import logging
import time


from pegasus_framework.core.config.config import config
from pegasus_framework.api.v1.schemas.generic import TokenInfo

logger = logging.getLogger(__name__)



class TokenHandler:
    def __init__(self):
        self.active_tokens: dict[str, TokenInfo] = {}

    def is_token_forced_valid(self, token: str, client_key: str) -> bool:
        """
            Toma el token y el clientKey y se fija si existe en las variables de entorno, con el fin de permitir
            Acceso sin autenticación desde el otro backend en laravel
        """        
        return (
            config.FORCED_VALID_TOKEN is not None and
            config.FORCED_CLIENT_KEY is not None and
            token == config.FORCED_VALID_TOKEN and
            client_key == config.FORCED_CLIENT_KEY
        )


    def verify_token(self, token: str, client_key: str) -> bool:
        if self.is_token_forced_valid(token, client_key):
            return True

        if self.is_token_cached(token, client_key):
            return True

        try:
            self.active_tokens[f"{token}:{client_key}"] = {
                "time": time.time(),
                "usuario_id": 1,
                "usuario_email": "xxx@sss.com",
            }
            return True
        except Exception as e:
            logger.error(f"Error verify_token: {e}")
            return False
    
    def decode_token(self, token: str, client_key: str) -> TokenInfo:
        logger.info(f"Decoding token: {token}")

        cache_key = f"{token}:{client_key}"

        if self.is_token_forced_valid(token, client_key):
            self.active_tokens[cache_key] = {
                "time": time.time(),
                "usuario_id": 1,
                "usuario_email": "config.FORCED_VALID_USER_EMAIL",
            }
            return self.active_tokens[cache_key]

        if self.is_token_cached(token, client_key):
            return self.active_tokens[cache_key]

        # simulación DB
        self.active_tokens[cache_key] = {
            "time": time.time(),
            "usuario_id": 1,
            "usuario_email": "xxx@sss.com",
        }
        return self.active_tokens[cache_key]
    
    def is_token_cached(self, token: str, client_key: str) -> bool:
        cache_key = f"{token}:{client_key}"
        if(cache_key in self.active_tokens):
            # se verifica si el token está en caché, se considera valido en cache durante 20 minutos (1200 segundos)
            if(time.time() - self.active_tokens[cache_key]["time"] < 1200):
                return True
            else:
                del self.active_tokens[cache_key]    
        return False

