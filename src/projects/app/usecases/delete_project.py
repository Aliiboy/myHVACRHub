from uuid import UUID

from projects.app.repositories.project_interface import ProjectRepositoryInterface


class DeleteProjectUseCase:
    """Cas d'utilisation pour supprimer un projet existant

    Cette classe implémente la logique métier nécessaire pour supprimer
    un projet existant dans la base de données en utilisant son identifiant.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour supprimer un projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, project_id: UUID) -> None:
        """Exécute le cas d'utilisation pour supprimer un projet

        Args:
            project_id (UUID): Identifiant unique du projet à supprimer

        Returns:
            None
        """
        self.repository.delete_project_by_id(project_id)
