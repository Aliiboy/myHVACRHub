import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.get_user_projects import GetUserProjectsUseCase
from projects.domain.entities.project_entity import ProjectEntity


class TestGetUserProjectsUseCase(unittest.TestCase):
    """Test de la récupération des projets d'un utilisateur

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la récupération des projets d'un utilisateur

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: GetUserProjectsUseCase = GetUserProjectsUseCase(
            repository=self.mock_project_repository,
        )

    def test_get_user_projects_returns_empty_list_when_no_projects(self) -> None:
        """Test de la récupération des projets d'un utilisateur sans projets

        Returns:
            None
        """
        # Arrange
        user_id = uuid4()
        cast(
            MagicMock, self.mock_project_repository.get_user_projects
        ).return_value = []

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.assertEqual(result, [])
        cast(
            MagicMock, self.mock_project_repository.get_user_projects
        ).assert_called_once_with(user_id)

    def test_get_user_projects_returns_projects_when_projects_exist(self) -> None:
        """Test de la récupération des projets d'un utilisateur avec des projets existants

        Returns:
            None
        """
        # Arrange
        user_id = uuid4()
        expected_projects = [
            ProjectEntity(
                project_number="PROJ-001",
                name="Premier projet",
                description="Description du premier projet",
            ),
            ProjectEntity(
                project_number="PROJ-002",
                name="Deuxième projet",
                description="Description du deuxième projet",
            ),
        ]
        cast(
            MagicMock, self.mock_project_repository.get_user_projects
        ).return_value = expected_projects

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.assertEqual(len(result), len(expected_projects))
        self.assertEqual(result, expected_projects)
        cast(
            MagicMock, self.mock_project_repository.get_user_projects
        ).assert_called_once_with(user_id)
