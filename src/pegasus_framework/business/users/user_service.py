from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork
from pegasus_framework.business.users.user_repository import UserRepository

class UserService:
    def __init__(self, uow: SqlAlchemyUnitOfWork):
        self.uow = uow
        self.repo = UserRepository(uow)

    def get_by_email(self, email: str):
        return self.repo.get_by_email(email)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)  