from pydantic import ValidationError

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectUpdateSchema
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import (
    ProjectValidationException,
)


class UpdateProjectUseCase:
    """Cas d'utilisation pour mettre à jour un projet existant

    Cette classe implémente la logique métier nécessaire pour mettre à jour
    un projet existant dans la base de données en utilisant le schéma
    de validation ProjectUpdateSchema.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour mettre à jour un projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, schema: ProjectUpdateSchema) -> ProjectEntity:
        """Exécute le cas d'utilisation pour mettre à jour un projet

        Args:
            schema (ProjectUpdateSchema): Schéma de validation pour la mise à jour d'un projet

        Raises:
            ProjectValidationException: Exception de validation

        Returns:
            ProjectEntity: Projet mis à jour
        """
        try:
            # Créer l'entité projet à partir du schéma
            project_to_update = ProjectEntity(
                id=schema.id,
                project_number=schema.project_number,
                name=schema.name,
                description=schema.description,
            )

            # Mettre à jour le projet
            return self.repository.update_project(project_to_update)
        except ValidationError as e:
            raise ProjectValidationException(e.errors())
