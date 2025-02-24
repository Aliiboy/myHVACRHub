from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import asc, select

from common.infra.data.sql_unit_of_work import SQLUnitOfWork
from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserDBException
from users.domain.services.password_hasher_interface import PasswordHasherInterface
from users.infra.data.models.user_sqlmodel import UserSQLModel


class UserSQLRepository(UserRepositoryInterface):
    def __init__(
        self, unit_of_work: SQLUnitOfWork, password_hasher: PasswordHasherInterface
    ):
        self.unit_of_work = unit_of_work
        self.password_hasher = password_hasher

    # write
    def sign_up_user(self, schema: UserEntity) -> UserEntity:
        try:
            hashed_password = self.password_hasher.hash(schema.password)
            with self.unit_of_work as uow:
                query = UserSQLModel(
                    id=schema.id,
                    email=schema.email,
                    password=hashed_password,
                    role=schema.role,
                    created_at=schema.created_at,
                )
                uow.session.add(query)
                uow.session.flush()
                return query.to_entity()
        except IntegrityError as e:
            raise UserDBException(message=str(e.orig))

    def delete_user_by_id(self, user_id: UUID) -> None:
        with self.unit_of_work as uow:
            user_to_delete = uow.session.get(UserSQLModel, user_id)
            if not user_to_delete:
                raise UserDBException(
                    message=f"L'utilisateur avec l'id '{user_id}' n'existe pas."
                )
            uow.session.delete(user_to_delete)
            uow.session.flush()

    # read
    def login_user(self, schema: UserEntity) -> UserEntity:
        with self.unit_of_work as uow:
            query = select(UserSQLModel).where(UserSQLModel.email == schema.email)
            user = uow.session.exec(query).first()

            if not user:
                raise UserDBException(
                    message=f"L'utilisateur avec l'email '{schema.email}' n'existe pas."
                )

            if not self.password_hasher.verify(schema.password, user.password):
                raise UserDBException(message="Mot de passe incorrect.")

            return user.to_entity()

    def get_all_users_with_limit(self, limit: int) -> list[UserEntity]:
        with self.unit_of_work as uow:
            query = select(UserSQLModel).order_by(asc(UserSQLModel.email)).limit(limit)
            users = uow.session.exec(query).all()
            return [user.to_entity() for user in users]
