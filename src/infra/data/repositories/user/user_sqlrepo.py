from sqlmodel import select

from domain.entities.user.user_entity import User
from infra.data.models.user.user_sqlmodel import UserSQLModel
from infra.data.repositories.user.user_interface import UserRepositoryInterface
from infra.data.sql_unit_of_work import SQLUnitOfWork


class UserSQLRepository(UserRepositoryInterface):
    def __init__(self, uow: SQLUnitOfWork):
        self.uow = uow

    def add_user(self, user: User) -> User:
        with self.uow as uow:
            query = UserSQLModel(
                id=user.id,
                email=user.email,
                hashed_password=user.hashed_password,
                created_at=user.created_at,
            )
            uow.session.add(query)
            uow.session.flush()
            uow.session.refresh(query)
            return query.to_entity()

    def get_user_by_email(self, email: str) -> User | None:
        with self.uow as uow:
            query = select(UserSQLModel).where(UserSQLModel.email == email)

            user_model = uow.session.exec(query).first()
            return user_model.to_entity() if user_model else None
