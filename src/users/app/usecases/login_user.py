from pydantic import ValidationError

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.schemas.user_schema import UserLoginSchema
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserValidationException
from users.domain.services.token_service_interface import TokenServiceInterface


class UserLoginUseCase:
    """Cas d'utilisation pour connecter un utilisateur

    Cette classe implémente la logique métier nécessaire pour connecter
    un utilisateur à la base de données en utilisant son email et son mot de passe.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
        token_service: TokenServiceInterface,
    ):
        """Initialise le cas d'utilisation pour connecter un utilisateur

        Args:
            repository (UserRepositoryInterface): Repository de l'utilisateur
            token_service (TokenServiceInterface): Service de génération de jetons
        """
        self.repository = repository
        self.token_service = token_service

    def execute(self, schema: UserLoginSchema) -> str:
        """Exécute la connexion d'un utilisateur

        Args:
            schema (UserLoginSchema): Schéma de connexion d'un utilisateur

        Raises:
            UserValidationException: Exception de validation

        Returns:
            str: Jeton généré
        """
        try:
            user_to_login = UserEntity(email=schema.email, password=schema.password)
            user_in_db = self.repository.login_user(user_to_login)
            return self.token_service.generate_token(
                user_id=user_in_db.id, role=user_in_db.role
            )
        except ValidationError as e:
            raise UserValidationException(e.errors())
