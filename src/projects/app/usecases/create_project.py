from uuid import UUID

from pydantic import ValidationError

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectCreateSchema
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import ProjectValidationException


class CreateProjectUseCase:
    """Cas d'utilisation pour créer un nouveau projet

    Cette classe implémente la logique métier nécessaire pour créer
    un nouveau projet dans la base de données en utilisant le schéma
    de validation ProjectCreateSchema.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour créer un nouveau projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, schema: ProjectCreateSchema, creator_id: UUID) -> ProjectEntity:
        """Exécute le cas d'utilisation pour créer un nouveau projet

        Args:
            schema (ProjectCreateSchema): Schéma de validation d'un nouveau projet
            creator_id (UUID): Identifiant de l'utilisateur créateur

        Raises:
            ProjectValidationException: Exception de validation

        Returns:
            ProjectEntity: Projet créé
        """
        try:
            project_to_create = ProjectEntity(
                project_number=schema.project_number,
                name=schema.name,
                description=schema.description,
            )
            return self.repository.create_project(
                schema=project_to_create, creator_id=creator_id
            )
        except ValidationError as e:
            raise ProjectValidationException(e.errors())
