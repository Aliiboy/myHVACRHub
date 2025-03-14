import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.delete_project import DeleteProjectUseCase


class TestDeleteProjectUseCase(unittest.TestCase):
    """Test de la suppression d'un projet par son id

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la suppression d'un projet par son id

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: DeleteProjectUseCase = DeleteProjectUseCase(
            repository=self.mock_project_repository,
        )

    def test_delete_project_success(self) -> None:
        """Test de la suppression d'un projet par son id

        Returns:
            None
        """
        self.use_case.execute(uuid4())
        cast(
            MagicMock, self.mock_project_repository.delete_project_by_id
        ).assert_called_once()
