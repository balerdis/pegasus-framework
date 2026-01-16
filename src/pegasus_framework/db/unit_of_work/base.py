# pegasus_framework/db/unit_of_work/base.py
from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    def __init__(self):
        self._committed = False

    @abstractmethod
    def _commit(self) -> None:
        ...

    def commit(self) -> None:
        self._commit()
        self._committed = True

    @abstractmethod
    def rollback(self) -> None:
        ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
        else:
            if not self._committed:
                raise RuntimeError(
                    "UnitOfWork exited without commit()"
                )
