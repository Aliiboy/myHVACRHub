import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.get_all_projects import GetAllProjectsUseCase
from projects.domain.entities.project_entity import ProjectEntity


class TestGetAllProjectsUseCase(unittest.TestCase):
    """Test de la récupération de tous les projets

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la récupération de tous les projets

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: GetAllProjectsUseCase = GetAllProjectsUseCase(
            repository=self.mock_project_repository,
        )

    def test_get_all_projects_success(self) -> None:
        """Test de la récupération de tous les projets

        Returns:
            None
        """
        # Arrange
        limit = 10
        expected_projects = [
            ProjectEntity(
                id=uuid4(),
                project_number="PROJ-001",
                name="Test Project",
                description="Test Description",
            ),
            ProjectEntity(
                id=uuid4(),
                project_number="PROJ-002",
                name="Test Project 2",
                description="Test Description 2",
            ),
        ]
        cast(
            MagicMock, self.mock_project_repository.get_all_projects_with_limit
        ).return_value = expected_projects

        # Act
        result = self.use_case.execute(limit)

        # Assert
        self.assertEqual(result, expected_projects)
        cast(
            MagicMock, self.mock_project_repository.get_all_projects_with_limit
        ).assert_called_once_with(limit)
