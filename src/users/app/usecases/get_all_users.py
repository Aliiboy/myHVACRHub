from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity


class GetAllUsersUsecase:
    """Cas d'utilisation pour récupérer tous les utilisateurs avec une limite

    Cette classe implémente la logique métier nécessaire pour récupérer
    tous les utilisateurs de la base de données avec une limite spécifiée.
    """

    def __init__(self, repository: UserRepositoryInterface):
        """Initialise le cas d'utilisation pour récupérer tous les utilisateurs avec une limite

        Args:
            repository (UserRepositoryInterface): Repository de l'utilisateur
        """
        self.repository = repository

    def execute(self, limit: int) -> list[UserEntity]:
        """Exécute la récupération de tous les utilisateurs avec une limite

        Args:
            limit (int): Limite de récupération

        Returns:
            list[UserEntity]: Liste des utilisateurs récupérés
        """
        return self.repository.get_all_users_with_limit(limit)
