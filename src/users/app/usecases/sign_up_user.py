from pydantic import ValidationError

from users.app.repositories.user_interface import UserRepositoryInterface
from users.app.schemas.user_schema import UserSignUpSchema
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import UserValidationException


class UserSignUpUseCase:
    """Cas d'utilisation pour enregistrer un nouvel utilisateur

    Cette classe implémente la logique métier nécessaire pour enregistrer
    un nouvel utilisateur dans la base de données en utilisant le schéma
    de validation UserSignUpSchema.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour enregistrer un nouvel utilisateur

        Args:
            repository (UserRepositoryInterface): Repository de l'utilisateur
        """
        self.repository = repository

    def execute(self, schema: UserSignUpSchema) -> UserEntity:
        """Exécute le cas d'utilisation pour enregistrer un nouvel utilisateur

        Args:
            schema (UserSignUpSchema): Schéma de validation d'un nouvel utilisateur

        Raises:
            UserValidationException: Exception de validation

        Returns:
            UserEntity: Entité d'utilisateur
        """
        try:
            user_to_sign_up = UserEntity(email=schema.email, password=schema.password)
            return self.repository.sign_up_user(user_to_sign_up)
        except ValidationError as e:
            raise UserValidationException(e.errors())
