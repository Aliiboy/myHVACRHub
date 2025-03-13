from uuid import UUID

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.domain.entities.project_entity import ProjectEntity


class GetProjectByIdUseCase:
    """Cas d'utilisation pour récupérer un projet par son identifiant

    Cette classe implémente la logique métier nécessaire pour récupérer
    un projet existant dans la base de données en utilisant son identifiant unique.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour récupérer un projet par son identifiant

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, project_id: UUID) -> ProjectEntity:
        """Exécute le cas d'utilisation pour récupérer un projet par son identifiant

        Args:
            project_id (UUID): Identifiant unique du projet à récupérer

        Returns:
            ProjectEntity: Projet récupéré
        """
        return self.repository.get_project_by_id(project_id)
