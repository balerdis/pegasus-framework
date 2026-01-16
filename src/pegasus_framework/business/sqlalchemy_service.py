# pegasus_framework/business/sqlalchemy_service.py
from pegasus_framework.business.base_service import BaseService
from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork

class SqlAlchemyService(BaseService):
    uow_cls = SqlAlchemyUnitOfWork