# pegasus_framework/api/middleware/rate_limit/in_memory_rate_limiter.py
import time
from collections import defaultdict
from threading import Lock

class InMemoryRateLimiter:
    def __init__(self):
        self._store = defaultdict(list)
        self._lock = Lock()

    def allow(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        window_start = now - window

        with self._lock:
            timestamps = self._store[key]

            # eliminar requests fuera de la ventana
            while timestamps and timestamps[0] < window_start:
                timestamps.pop(0)

            if len(timestamps) >= limit:
                return False

            timestamps.append(now)
            return True
