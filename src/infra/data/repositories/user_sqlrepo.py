from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.repositories.user_interface import UserRepositoryInterface
from domain.entities.user.user_entity import User
from domain.exceptions.user_exceptions import (
    UserAlreadyExistsException,
)
from infra.data.models.user_sqlmodel import UserSQLModel
from infra.data.sql_unit_of_work import SQLUnitOfWork


class UserSQLRepository(UserRepositoryInterface):
    def __init__(self, uow: SQLUnitOfWork):
        self.uow = uow

    def add_user(self, user: User) -> User:
        try:
            with self.uow as uow:
                query = UserSQLModel(
                    id=user.id,
                    email=user.email,
                    hashed_password=user.hashed_password,
                    role=user.role,
                    created_at=user.created_at,
                )
                uow.session.add(query)
                uow.session.flush()
                return query.to_entity()
        except IntegrityError:
            raise UserAlreadyExistsException(query.email)

    def get_user_by_email(self, email: str) -> User | None:
        with self.uow as uow:
            query = select(UserSQLModel).where(UserSQLModel.email == email)

            user_model = uow.session.exec(query).first()
            return user_model.to_entity() if user_model else None
