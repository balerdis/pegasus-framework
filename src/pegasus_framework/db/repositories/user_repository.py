# pegasus_framework/db/repositories/user_repository.py
from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from pegasus_framework.core.exceptions.domain.entity_not_found import EntityNotFoundError
from pegasus_framework.auth.models.users.registry import get_user_model
from pegasus_framework.auth.models.users.user_base import BaseUser
from typing import Optional, Type

class UserRepository(BaseRepository[BaseUser]):
    def __init__(self, session: Session):
        model: Type[BaseUser] = get_user_model()
        super().__init__(model, session)

    def get_by_email(self, email: str) -> Optional[BaseUser]:
        smt = self._base_query().where(self.model_class.email == email)
        return self.session.execute(smt).scalar_one_or_none()
    
    def get_by_email_or_fail(self, email: str):
        db_obj = self.get_by_email(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model_class.__name__} con email={email} no encontrado")
        return db_obj    