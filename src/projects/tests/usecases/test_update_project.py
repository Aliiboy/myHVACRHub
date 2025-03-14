import unittest
from datetime import datetime, timezone
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectUpdateSchema
from projects.app.usecases.update_project import UpdateProjectUseCase
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import ProjectValidationException
from projects.domain.settings.project_settings import ProjectSettings


class TestUpdateProjectUseCase(unittest.TestCase):
    """Test de la mise à jour d'un projet

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de la mise à jour d'un projet

        Returns:
            None
        """
        self.mock_project_repository: MagicMock = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case: UpdateProjectUseCase = UpdateProjectUseCase(
            repository=self.mock_project_repository,
        )

    def test_update_project_success(self) -> None:
        """Test de la mise à jour d'un projet

        Returns:
            None
        """
        # Arrange
        project_id = uuid4()
        created_at = datetime.now(timezone.utc)
        update_schema = ProjectUpdateSchema(
            id=project_id,
            project_number="PROJ-001",
            name="Updated Project",
            description="Updated Description",
        )
        expected_project = ProjectEntity(
            id=project_id,
            project_number="PROJ-001",
            name="Updated Project",
            description="Updated Description",
            created_at=created_at,
            updated_at=datetime.now(timezone.utc),
        )
        cast(
            MagicMock, self.mock_project_repository.update_project
        ).return_value = expected_project

        # Act
        result = self.use_case.execute(update_schema)

        # Assert
        self.assertEqual(result, expected_project)
        self.assertNotEqual(result.created_at, result.updated_at)
        self.assertGreater(result.updated_at, result.created_at)
        cast(
            MagicMock, self.mock_project_repository.update_project
        ).assert_called_once()

    def test_update_project_validation_error(self) -> None:
        """Test de la mise à jour d'un projet avec une erreur de validation

        Returns:
            None
        """
        # Arrange
        update_schema = ProjectUpdateSchema(
            id=uuid4(),
            project_number="A" * ProjectSettings.project_number_max_length + "1",
            name="Updated Project",
            description="Updated Description",
        )

        # Act & Assert
        with self.assertRaises(ProjectValidationException):
            self.use_case.execute(update_schema)
