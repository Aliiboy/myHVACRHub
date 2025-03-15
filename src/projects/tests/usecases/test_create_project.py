import unittest
from typing import cast
from unittest.mock import MagicMock
from uuid import uuid4

from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.app.schemas.project_schema import ProjectCreateSchema
from projects.app.usecases.create_project import CreateProjectUseCase
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import ProjectValidationException
from projects.domain.settings.project_settings import ProjectSettings


class TestCreateProjectUseCase(unittest.TestCase):
    """Tests du cas d'utilisation de création d'un projet

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des usecases
    """

    def setUp(self) -> None:
        """Initialise le testeur de création d'un projet

        Returns:
            None
        """
        self.mock_project_repository: ProjectRepositoryInterface = MagicMock(
            spec=ProjectRepositoryInterface
        )
        self.use_case = CreateProjectUseCase(
            repository=self.mock_project_repository,
        )

    def test_create_project_success(self) -> None:
        """Test de la création d'un projet avec succès

        Returns:
            None
        """
        project_id = uuid4()
        creator_id = uuid4()
        # Arrange - Préparer les données de test et le comportement attendu
        project_schema = ProjectCreateSchema(
            project_number="PRJ-001",
            name="Projet Test",
            description="Description du projet de test",
        )

        # Configurer le mock pour retourner une entité projet avec l'ID spécifié
        mock_project_entity = ProjectEntity(
            id=project_id,
            project_number=project_schema.project_number,
            name=project_schema.name,
            description=project_schema.description,
        )
        cast(
            MagicMock, self.mock_project_repository.create_project
        ).return_value = mock_project_entity

        # Act - Exécuter le cas d'utilisation
        result = self.use_case.execute(schema=project_schema, creator_id=creator_id)

        # Assert - Vérifier les résultats et comportements attendus
        cast(
            MagicMock, self.mock_project_repository.create_project
        ).assert_called_once()
        self.assertEqual(result.id, project_id)
        self.assertEqual(result.project_number, project_schema.project_number)
        self.assertEqual(result.name, project_schema.name)
        self.assertEqual(result.description, project_schema.description)

    def test_create_project_with_validation_error(self) -> None:
        """Test de la création d'un projet avec erreur de validation

        Returns:
            None
        """
        creator_id = uuid4()
        # Créer un schéma invalid pour le test
        invalid_project_schema = ProjectCreateSchema(
            project_number="A" * (ProjectSettings.project_number_max_length + 1),
            name="A" * (ProjectSettings.name_max_length + 1),
            description="A" * (ProjectSettings.description_max_length + 1),
        )

        # Act & Assert - On s'attend à une exception lorsque le cas d'utilisation est exécuté
        with self.assertRaises(ProjectValidationException) as context:
            self.use_case.execute(schema=invalid_project_schema, creator_id=creator_id)

        # Assert - Vérifier que l'exception est levée
        self.assertIsInstance(context.exception, ProjectValidationException)
        self.assertTrue(len(context.exception.errors) > 0)
        self.assertEqual(context.exception.errors[0]["field"], "project_number")
        self.assertEqual(context.exception.errors[1]["field"], "name")
        self.assertEqual(context.exception.errors[2]["field"], "description")
