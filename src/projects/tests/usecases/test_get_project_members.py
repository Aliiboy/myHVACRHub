import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.usecases.get_project_members import GetProjectMembersUseCase
from users.domain.entities.user_entity import UserEntity


class TestGetProjectMembersUseCase(unittest.TestCase):
    """Test de la récupération des membres d'un projet

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la récupération des membres d'un projet

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: GetProjectMembersUseCase = GetProjectMembersUseCase(
            repository=self.mock_project_repository,
        )

    def test_get_project_members_returns_empty_list_when_no_members(self) -> None:
        """Test de la récupération des membres d'un projet sans membres

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        cast(
            MagicMock, self.mock_project_repository.get_project_members
        ).return_value = []

        # Act
        result = self.use_case.execute(project_id)

        # Assert
        self.assertEqual(result, [])
        cast(
            MagicMock, self.mock_project_repository.get_project_members
        ).assert_called_once_with(project_id)

    def test_get_project_members_returns_members_when_members_exist(self) -> None:
        """Test de la récupération des membres d'un projet avec des membres existants

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        expected_members = [
            UserEntity(
                email="member1@example.com",
                password="Password_1234!",
            ),
            UserEntity(
                email="member2@example.com",
                password="Password_1234!",
            ),
        ]
        cast(
            MagicMock, self.mock_project_repository.get_project_members
        ).return_value = expected_members

        # Act
        result = self.use_case.execute(project_id)

        # Assert
        self.assertEqual(len(result), len(expected_members))
        self.assertEqual(result, expected_members)
        cast(
            MagicMock, self.mock_project_repository.get_project_members
        ).assert_called_once_with(project_id)
