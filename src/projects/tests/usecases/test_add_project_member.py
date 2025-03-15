import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectAddMemberSchema
from projects.app.usecases.add_project_member import AddProjectMemberUseCase
from projects.domain.entities.project_entity import (
    ProjectAndUserJonctionTableEntity,
    ProjectMemberRole,
)


class TestAddProjectMemberUseCase(unittest.TestCase):
    """Test de l'ajout d'un membre à un projet

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de l'ajout d'un membre à un projet

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: AddProjectMemberUseCase = AddProjectMemberUseCase(
            repository=self.mock_project_repository,
        )

    def test_add_project_member_success(self) -> None:
        """Test de l'ajout d'un membre à un projet avec succès

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        user_id = uuid4()
        role = ProjectMemberRole.MEMBER

        schema = ProjectAddMemberSchema(
            project_id=project_id,
            user_id=user_id,
        )
        expected_member = ProjectAndUserJonctionTableEntity(
            project_id=project_id,
            user_id=user_id,
            role=role,
        )
        cast(
            MagicMock, self.mock_project_repository.add_project_member
        ).return_value = expected_member

        # Act
        result = self.use_case.execute(schema=schema)
        # Assert
        self.assertEqual(result.project_id, expected_member.project_id)
        self.assertEqual(result.user_id, expected_member.user_id)
        self.assertEqual(result.role, expected_member.role)
        cast(
            MagicMock, self.mock_project_repository.add_project_member
        ).assert_called_once_with(project_id=project_id, user_id=user_id, role=role)
