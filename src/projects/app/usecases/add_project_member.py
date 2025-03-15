from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectAddMemberSchema
from projects.domain.entities.project_entity import ProjectAndUserJonctionTableEntity


class AddProjectMemberUseCase:
    """Cas d'utilisation pour ajouter un membre à un projet

    Cette classe implémente la logique métier nécessaire pour ajouter
    un membre à un projet existant dans la base de données.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour ajouter un membre à un projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(
        self, schema: ProjectAddMemberSchema
    ) -> ProjectAndUserJonctionTableEntity:
        """Exécute le cas d'utilisation pour ajouter un membre à un projet

        Args:
            schema (ProjectAddMemberSchema): Schéma de validation pour l'ajout d'un membre

        Returns:
            ProjectAndUserJonctionTableEntity: Lien créé entre le projet et le membre
        """
        member_to_add = ProjectAndUserJonctionTableEntity(
            project_id=schema.project_id,
            user_id=schema.user_id,
        )
        return self.repository.add_project_member(
            project_id=member_to_add.project_id,
            user_id=member_to_add.user_id,
            role=member_to_add.role,
        )
