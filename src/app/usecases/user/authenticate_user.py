from domain.services.password_hasher_interface import PasswordHasherInterface
from domain.services.token_service_interface import TokenServiceInterface
from infra.data.repositories.user.user_interface import UserRepositoryInterface


class AuthenticateUserUseCase:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
        token_service: TokenServiceInterface,
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, email: str, password: str) -> str:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("Email incorrect.")

        if not self.password_hasher.verify(password, user.hashed_password):
            raise ValueError("Mot de passe incorrect.")

        return self.token_service.generate_token(user_id=user.id, role=user.role)
