from datetime import datetime, timedelta
from uuid import UUID

import jwt

from users.domain.entities.user_entity import UserRole
from users.domain.services.token_service_interface import TokenServiceInterface


class JWTTokenService(TokenServiceInterface):
    """Service pour la génération de jetons JWT

    Args:
        secret_key (str): Clé secrète pour le jeton
        algorithm (str): Algorithme pour le jeton
        expires_delta (timedelta | None): Délai d'expiration du jeton
    """

    def __init__(
        self, secret_key: str, algorithm: str, expires_delta: timedelta | None = None
    ):
        """Initialise le service pour la génération de jetons JWT

        Args:
            secret_key (str): Clé secrète pour le jeton
            algorithm (str): Algorithme pour le jeton
            expires_delta (timedelta | None, optional): Délai d'expiration du jeton. Defaults to None.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def generate_token(self, user_id: UUID, role: UserRole) -> str:
        """Génère un jeton pour un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur
            role (UserRole): Rôle de l'utilisateur

        Returns:
            str: Jeton généré
        """
        payload: dict[str, str | int] = {
            "sub": str(user_id),
            "role": role,
        }
        if self.expires_delta is not None:
            expiration_time = datetime.utcnow() + self.expires_delta
            payload["exp"] = int(expiration_time.timestamp())
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
