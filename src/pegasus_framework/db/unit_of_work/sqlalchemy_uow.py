# pegasus_framework/db/unit_of_work/sqlalchemy_uow.py
from sqlalchemy.orm import Session
from pegasus_framework.db.connection import db_connection
from pegasus_framework.db.unit_of_work.base import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__()
        self._session: Session | None = None

    def commit(self):
        self._get_session().commit()

    def _get_session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork is not active")
        return self._session
    
    def __enter__(self):
        self._session = db_connection.create_session()
        return self

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()

    def repo(self, repo_cls):
        impl = self.resolve_repository(repo_cls)
        return impl(self._get_session())

    def __exit__(self, exc_type, exc, tb):
        try:
            super().__exit__(exc_type, exc, tb)
        finally:
            if self._session is not None:
                self._session.close()
                self._session = None


