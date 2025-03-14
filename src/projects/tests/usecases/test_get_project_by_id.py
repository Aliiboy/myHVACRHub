import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.get_project_by_id import GetProjectByIdUseCase
from projects.domain.entities.project_entity import ProjectEntity


class TestGetProjectByIdUseCase(unittest.TestCase):
    """Test de la récupération d'un projet par son id

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la récupération d'un projet par son id

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: GetProjectByIdUseCase = GetProjectByIdUseCase(
            repository=self.mock_project_repository,
        )

    def test_get_project_by_id_success(self) -> None:
        """Test de la récupération d'un projet par son id

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        expected_project = ProjectEntity(
            id=project_id,
            project_number="PROJ-001",
            name="Test Project",
            description="Test Description",
        )
        cast(
            MagicMock, self.mock_project_repository.get_project_by_id
        ).return_value = expected_project

        # Act
        result = self.use_case.execute(project_id)

        # Assert
        self.assertEqual(result, expected_project)
        cast(
            MagicMock, self.mock_project_repository.get_project_by_id
        ).assert_called_once_with(project_id)
