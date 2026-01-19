class InvalidAuthSessionError(Exception):
    """
    El auth session error: el access token es inválido, expirado o su sesión fue revocada.
    """
    pass
