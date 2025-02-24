from pydantic import ValidationError

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.schemas.user_schema import UserSignUpSchema
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserValidationException


class UserSignUpUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self.repository = repository

    def execute(self, schema: UserSignUpSchema) -> UserEntity:
        try:
            user_to_sign_up = UserEntity(email=schema.email, password=schema.password)
            return self.repository.sign_up_user(user_to_sign_up)
        except ValidationError as e:
            raise UserValidationException(e.errors())
