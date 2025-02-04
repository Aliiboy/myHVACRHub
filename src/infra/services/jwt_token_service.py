from datetime import datetime, timedelta

import jwt

from domain.services.token_service_interface import TokenServiceInterface


class JWTTokenService(TokenServiceInterface):
    def __init__(
        self, secret_key: str, algorithm: str, expires_delta: timedelta | None = None
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def generate_token(self, user_id: str) -> str:
        payload: dict[str, str | int] = {"sub": str(user_id)}

        if self.expires_delta is not None:
            expiration_time = datetime.utcnow() + self.expires_delta
            payload["exp"] = int(expiration_time.timestamp())

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
