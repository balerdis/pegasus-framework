# pegasus_framework/wiring/providers.py
from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork

def provide_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork()