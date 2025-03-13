from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.domain.entities.project_entity import ProjectEntity


class GetAllProjectsUseCase:
    """Cas d'utilisation pour récupérer tous les projets avec une limite

    Cette classe implémente la logique métier nécessaire pour récupérer
    une liste limitée de projets depuis la base de données.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour récupérer tous les projets

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, limit: int) -> list[ProjectEntity]:
        """Exécute le cas d'utilisation pour récupérer tous les projets avec une limite

        Args:
            limit (int): Nombre maximum de projets à récupérer.

        Returns:
            list[ProjectEntity]: Liste des projets récupérés
        """
        return self.repository.get_all_projects_with_limit(limit)
