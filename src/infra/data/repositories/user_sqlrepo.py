from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.repositories.user_interface import UserRepositoryInterface
from domain.entities.user.user_entity import User
from domain.exceptions.user_exceptions import (
    UserAlreadyExistsException,
)
from domain.services.password_hasher_interface import PasswordHasherInterface
from infra.data.models.user_sqlmodel import UserSQLModel
from infra.data.sql_unit_of_work import SQLUnitOfWork


class UserSQLRepository(UserRepositoryInterface):
    def __init__(
        self, unit_of_work: SQLUnitOfWork, password_hasher: PasswordHasherInterface
    ):
        self.unit_of_work = unit_of_work
        self.password_hasher = password_hasher

    def add_user(self, user: User) -> User:
        try:
            hashed_password = self.password_hasher.hash(user.password)
            with self.unit_of_work as uow:
                query = UserSQLModel(
                    id=user.id,
                    email=user.email,
                    password=hashed_password,
                    role=user.role,
                    created_at=user.created_at,
                )
                uow.session.add(query)
                uow.session.flush()
                return query.to_entity()
        except IntegrityError:
            raise UserAlreadyExistsException(query.email)

    def get_user_by_email(self, email: str) -> User | None:
        with self.unit_of_work as uow:
            query = select(UserSQLModel).where(UserSQLModel.email == email)

            user = uow.session.exec(query).first()
            return user.to_entity() if user else None

    def get_all_users(self, limit: int) -> list[User]:
        with self.unit_of_work as uow:
            query = select(UserSQLModel).limit(limit)

            users = uow.session.exec(query).all()
            return [user.to_entity() for user in users]
