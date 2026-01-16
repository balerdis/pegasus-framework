# pegasus_framework/business/base_service.py
from pegasus_framework.db.unit_of_work.base import UnitOfWork

class BaseService:
    uow_cls: type[UnitOfWork]

    def _uow(self) -> UnitOfWork:
        if not hasattr(self, "uow_cls"):
            raise RuntimeError(
                f"{self.__class__.__name__} must define uow_cls"
            )
        return self.uow_cls()