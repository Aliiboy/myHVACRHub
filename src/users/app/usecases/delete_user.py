from uuid import UUID

from users.app.repositories.user_interface import UserRepositoryInterface


class DeleteUserByIdUsecase:
    """Cas d'utilisation pour supprimer un utilisateur par son identifiant

    Cette classe implémente la logique métier nécessaire pour supprimer
    un utilisateur de la base de données en utilisant son UUID.
    """

    def __init__(self, repository: UserRepositoryInterface):
        """Initialise le cas d'utilisation pour supprimer un utilisateur par son identifiant

        Args:
            repository (UserRepositoryInterface): Repository de l'utilisateur
        """
        self.repository = repository

    def execute(self, user_id: UUID) -> None:
        """Exécute la suppression d'un utilisateur par son identifiant

        Args:
            user_id (UUID): Identifiant de l'utilisateur à supprimer
        """
        return self.repository.delete_user_by_id(user_id)
