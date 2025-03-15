from uuid import UUID

from projects.app.repositories.project_interface import ProjectRepositoryInterface


class DeleteProjectMemberUseCase:
    """Cas d'utilisation pour supprimer un membre d'un projet

    Cette classe implémente la logique métier nécessaire pour supprimer
    un membre d'un projet existant dans la base de données.
    """

    def __init__(
        self,
        repository: ProjectRepositoryInterface,
    ):
        """Initialise le cas d'utilisation pour supprimer un membre d'un projet

        Args:
            repository (ProjectRepositoryInterface): Repository du projet
        """
        self.repository = repository

    def execute(self, project_id: UUID, user_id: UUID) -> None:
        """Exécute le cas d'utilisation pour supprimer un membre d'un projet

        Args:
            project_id (UUID): Identifiant du projet
            user_id (UUID): Identifiant de l'utilisateur

        Returns:
            None
        """
        self.repository.delete_project_member(project_id, user_id)
