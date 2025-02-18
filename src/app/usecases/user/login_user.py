from pydantic import ValidationError

from app.repositories.user_interface import UserRepositoryInterface
from app.schemas.user_schema import UserLoginSchema
from domain.entities.user.user_entity import UserEntity
from domain.exceptions.user_exceptions import UserValidationException
from domain.services.token_service_interface import TokenServiceInterface


class UserLoginUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        token_service: TokenServiceInterface,
    ):
        self.repository = repository
        self.token_service = token_service

    def execute(self, schema: UserLoginSchema) -> str:
        try:
            user_to_login = UserEntity(email=schema.email, password=schema.password)
            user_in_db = self.repository.login_user(user_to_login)
            return self.token_service.generate_token(
                user_id=user_in_db.id, role=user_in_db.role
            )
        except ValidationError as e:
            raise UserValidationException(e.errors())
