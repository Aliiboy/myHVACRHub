from datetime import datetime

import bcrypt
import jwt

from infra.data.repositories.user.user_interface import UserRepositoryInterface
from infra.web.settings import AppSettings


class AuthenticateUserUseCase:
    def __init__(self, repository: UserRepositoryInterface, settings: AppSettings):
        self.repository = repository
        self.settings = settings

    def execute(self, email: str, password: str) -> str:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("Email incorrect.")

        if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
            raise ValueError("Mot de passe incorrect.")

        payload: dict[str, str | int] = {"sub": str(user.id)}

        if self.settings.JWT_ACCESS_TOKEN_EXPIRES is not None:
            expiration_time = datetime.utcnow() + self.settings.JWT_ACCESS_TOKEN_EXPIRES
            payload["exp"] = int(expiration_time.timestamp())

        token = jwt.encode(
            payload, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ALGORITHM
        )

        return token
