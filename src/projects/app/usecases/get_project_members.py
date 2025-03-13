from uuid import UUID

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from users.domain.entities.user_entity import UserEntity


class GetProjectMembersUseCase:
    """Cas d'utilisation pour récupérer tous les membres d'un projet

    Cette classe implémente la logique métier nécessaire pour récupérer
    tous les utilisateurs qui sont membres d'un projet spécifique.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour récupérer les membres d'un projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, project_id: UUID) -> list[UserEntity]:
        """Exécute le cas d'utilisation pour récupérer tous les membres d'un projet

        Args:
            project_id (UUID): Identifiant du projet

        Returns:
            list[UserEntity]: Liste des membres du projet
        """
        return self.repository.get_project_members(project_id)
