import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.delete_project_member import DeleteProjectMemberUseCase


class TestDeleteProjectMemberUseCase(unittest.TestCase):
    """Test de la suppression d'un membre d'un projet

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la suppression d'un membre d'un projet

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: DeleteProjectMemberUseCase = DeleteProjectMemberUseCase(
            repository=self.mock_project_repository,
        )

    def test_delete_project_member_success(self) -> None:
        """Test de la suppression d'un membre d'un projet avec succès

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        user_id = uuid4()

        # Act
        self.use_case.execute(project_id, user_id)

        # Assert
        cast(
            MagicMock, self.mock_project_repository.delete_project_member
        ).assert_called_once_with(project_id, user_id)
