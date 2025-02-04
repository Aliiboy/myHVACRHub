import bcrypt

from domain.entities.user.user_entity import User
from infra.data.repositories.user.user_interface import UserRepositoryInterface


class CreateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def execute(self, email: str, password: str) -> User:
        existing_user = self.repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("L'email est déjà utilisé.")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User(email=email, hashed_password=hashed_password)

        self.repository.add_user(new_user)
        return new_user
