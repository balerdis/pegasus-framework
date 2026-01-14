from pegasus_framework.auth.models.users.registry import get_user_model
from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork
from pegasus_framework.db.repositories.base_repository import ModelType
from pegasus_framework.db.repositories.base_repository import EntityNotFoundError   
from sqlalchemy import select

class UserRepository:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow
        self.model = get_user_model()

    def get_by_email(self, email: str):
        stmt = (
            select(self.model)
            .where(self.model.email == email)
        )
        return self.uow.session.execute(stmt).scalar_one_or_none()

    def get_by_id(self, id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
        )
        return self.uow.session.execute(stmt).scalar_one_or_none()

    def get_by_id_or_fail(self, id: int) -> ModelType:
        db_obj = self.get_by_id(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model.__name__} con id={id} no encontrado")
        return db_obj

    def get_by_email_or_fail(self, email: str) -> ModelType:
        db_obj = self.get_by_email(email)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model.__name__} con email={email} no encontrado")
        return db_obj


        
    
