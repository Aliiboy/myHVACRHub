import unittest
from datetime import timedelta
from uuid import uuid4

import jwt

from users.domain.entities.user_entity import UserRole
from users.infra.services.jwt_token_service import JWTTokenService


class TestJWTTokenService(unittest.TestCase):
    """Test de la génération de jetons JWT

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des services
    """

    def setUp(self) -> None:
        """Initialise le testeur de la génération de jetons JWT

        Returns:
            None
        """
        self.secret_key = "testsecret"
        self.algorithm = "HS256"
        self.service = JWTTokenService(
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expires_delta=timedelta(seconds=1),
        )

    def test_generate_token(self) -> None:
        """Test de la génération de jetons JWT

        Returns:
            None
        """
        user_id = uuid4()
        role = UserRole.USER
        token = self.service.generate_token(user_id=user_id, role=role)

        decoded = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            options={"verify_exp": False},
        )

        self.assertEqual(decoded["sub"], str(user_id))
        self.assertEqual(decoded["role"], role)

    def test_generate_token_with_expiration(self) -> None:
        """Test de la génération de jetons JWT avec une expiration

        Returns:
            None
        """
        self.service = JWTTokenService(
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expires_delta=timedelta(seconds=1),
        )
        user_id = uuid4()
        token = self.service.generate_token(user_id=user_id, role=UserRole.ADMIN)

        decoded = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            options={"verify_exp": False},
        )
        self.assertIn("exp", decoded)
