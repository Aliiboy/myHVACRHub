from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domain.entities.user.user_entity import User
from infra.data.models.user.user_sqlmodel import UserSQLModel
from infra.data.repositories.user.user_interface import UserRepositoryInterface


class UserSQLRepository(UserRepositoryInterface):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def add_user(self, user: User) -> User:
        with self.session_factory() as session:
            query = UserSQLModel(
                id=user.id,
                email=user.email,
                hashed_password=user.hashed_password,
                created_at=user.created_at,
            )
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
                return query.to_entity()
            except IntegrityError as e:
                session.rollback()
                raise e

    def get_user_by_email(self, email: str) -> User | None:
        with self.session_factory() as session:
            query = select(UserSQLModel).where(UserSQLModel.email == email)
            user_model = session.exec(query).first()
            return user_model.to_entity() if user_model else None
