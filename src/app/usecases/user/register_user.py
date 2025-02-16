from pydantic import ValidationError

from app.repositories.user_interface import UserRepositoryInterface
from app.schemas.user_schema import UserSignUpSchema
from domain.entities.user.user_entity import User
from domain.exceptions.user_exceptions import UserValidationException


class UserSignUpUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self.repository = repository

    def execute(self, schema: UserSignUpSchema) -> User:
        try:
            user_to_add = User(email=schema.email, password=schema.password)
            return self.repository.add_user(user_to_add)
        except ValidationError as e:
            raise UserValidationException(e.errors())
