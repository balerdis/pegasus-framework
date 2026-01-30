# pegasus_framework/core/time/clock.py
from datetime import datetime
from .timezones import UTC

class Clock:
    """
    Proveedor de tiempo del framework.

    - Centraliza la obtención de 'now'
    - Facilita testing
    - Evita datetime.now() desperdigados
    """

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(tz=UTC)

    @staticmethod
    def now(tz) -> datetime:
        return datetime.now(tz=tz)
