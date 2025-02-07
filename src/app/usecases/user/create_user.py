from domain.entities.user.user_entity import User
from domain.services.password_hasher_interface import PasswordHasherInterface
from infra.data.repositories.user.user_interface import UserRepositoryInterface


class CreateUserUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
    ):
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str) -> User:
        hashed_password = self.password_hasher.hash(password)
        new_user = User(email=email, hashed_password=hashed_password)
        self.repository.add_user(new_user)

        return new_user
