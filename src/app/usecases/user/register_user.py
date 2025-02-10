from pydantic import ValidationError

from app.repositories.user_interface import UserRepositoryInterface
from domain.entities.user.user_entity import User
from domain.exceptions.user_exceptions import UserInvalidPasswordPatternException


class RegisterUserUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self.repository = repository

    def execute(self, email: str, password: str) -> User:
        try:
            new_user = User(email=email, password=password)
            self.repository.add_user(new_user)
        except ValidationError:
            raise UserInvalidPasswordPatternException()
        return new_user
