from uuid import UUID

from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity


class GetUserProfileUseCase:
    """Cas d'utilisation pour récupérer le profil d'un utilisateur

    Cette classe implémente la logique métier nécessaire pour récupérer
    le profil d'un utilisateur de la base de données en utilisant son UUID.
    """

    def __init__(self, repository: UserRepositoryInterface):
        """Initialise le cas d'utilisation pour récupérer le profil d'un utilisateur

        Args:
            repository (UserRepositoryInterface): Repository de l'utilisateur
        """
        self.repository = repository

    def execute(self, user_id: UUID) -> UserEntity:
        """Exécute la récupération du profil d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur à récupérer

        Returns:
            UserEntity: Utilisateur récupéré
        """
        return self.repository.get_user_profile(user_id)
