from uuid import UUID

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.domain.entities.project_entity import ProjectEntity


class GetUserProjectsUseCase:
    """Cas d'utilisation pour récupérer tous les projets d'un utilisateur

    Cette classe implémente la logique métier nécessaire pour récupérer
    tous les projets dont un utilisateur est membre.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour récupérer les projets d'un utilisateur

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, user_id: UUID) -> list[ProjectEntity]:
        """Exécute le cas d'utilisation pour récupérer tous les projets d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur

        Returns:
            list[ProjectEntity]: Liste des projets de l'utilisateur
        """
        return self.repository.get_user_projects(user_id)
