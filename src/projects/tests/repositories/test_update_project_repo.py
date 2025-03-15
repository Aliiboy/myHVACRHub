from datetime import timezone
from uuid import uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
)
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestUpdateProjectSQLRepository(TestBaseRepository):
    """Test de la mise à jour d'un projet

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de mise à jour d'un projet

        Returns:
            None
        """
        super().setUp()
        self.project_repository = ProjectSQLRepository(unit_of_work=self.uow)
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )

        # Créer un utilisateur pour être propriétaire du projet
        self.owner = UserEntity(email="owner@example.com", password="Password_1234!")
        self.owner = self.user_repository.sign_up_user(self.owner)

        # Créer un projet valide
        self.valid_project = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project",
            description="A test project",
        )
        self.project = self.project_repository.create_project(
            schema=self.valid_project, creator_id=self.owner.id
        )

        # Créer un second projet pour tester les contraintes d'unicité
        self.second_project = ProjectEntity(
            project_number="PRJ-002",
            name="Second Test Project",
            description="Another test project",
        )
        self.second_project = self.project_repository.create_project(
            schema=self.second_project, creator_id=self.owner.id
        )

    def test_update_project_success(self) -> None:
        """Test de la mise à jour d'un projet avec succès

        Returns:
            None
        """
        # Créer un projet mis à jour
        updated_project = ProjectEntity(
            id=self.project.id,
            project_number="PRJ-001-UPDATED",
            name="Test Project Updated",
            description="An updated test project",
        )

        # Mettre à jour le projet
        result = self.project_repository.update_project(updated_project)

        # Vérifier que le projet a été mis à jour
        self.assertEqual(updated_project.id, result.id)
        self.assertEqual(updated_project.project_number, result.project_number)
        self.assertEqual(updated_project.name, result.name)
        self.assertEqual(updated_project.description, result.description)

        # Vérifier que les timestamps sont correctement mis à jour
        self.assertNotEqual(result.created_at, result.updated_at)
        # Convertir les dates en UTC si nécessaire
        created_at_utc = (
            result.created_at.replace(tzinfo=timezone.utc)
            if result.created_at.tzinfo is None
            else result.created_at
        )
        updated_at_utc = (
            result.updated_at.replace(tzinfo=timezone.utc)
            if result.updated_at.tzinfo is None
            else result.updated_at
        )
        self.assertGreater(updated_at_utc, created_at_utc)

        # Récupérer le projet pour vérifier que les modifications ont été enregistrées
        retrieved_project = self.project_repository.get_project_by_id(self.project.id)
        self.assertEqual(
            updated_project.project_number, retrieved_project.project_number
        )
        self.assertEqual(updated_project.name, retrieved_project.name)
        self.assertEqual(updated_project.description, retrieved_project.description)
        self.assertNotEqual(retrieved_project.created_at, retrieved_project.updated_at)
        # Convertir les dates en UTC si nécessaire
        retrieved_created_at_utc = (
            retrieved_project.created_at.replace(tzinfo=timezone.utc)
            if retrieved_project.created_at.tzinfo is None
            else retrieved_project.created_at
        )
        retrieved_updated_at_utc = (
            retrieved_project.updated_at.replace(tzinfo=timezone.utc)
            if retrieved_project.updated_at.tzinfo is None
            else retrieved_project.updated_at
        )
        self.assertGreater(retrieved_updated_at_utc, retrieved_created_at_utc)

    def test_update_project_not_found(self) -> None:
        """Test de la mise à jour d'un projet qui n'existe pas

        Returns:
            None
        """
        # Créer un projet avec un ID inexistant
        non_existent_project = ProjectEntity(
            id=uuid4(),
            project_number="PRJ-NONEXISTENT",
            name="Non-existent Project",
            description="This project does not exist",
        )

        # Tenter de mettre à jour le projet
        with self.assertRaises(ProjectDBException) as context:
            self.project_repository.update_project(non_existent_project)

        expected_message = f"ProjectException : Le projet avec l'id '{non_existent_project.id}' n'existe pas."
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_update_project_duplicate_name(self) -> None:
        """Test de la mise à jour d'un projet avec un nom déjà utilisé

        Returns:
            None
        """
        # Mettre à jour le premier projet avec le nom du second
        updated_project = ProjectEntity(
            id=self.project.id,
            project_number="PRJ-001",
            name=self.second_project.name,  # Nom déjà utilisé par le second projet
            description="Updated description",
        )

        # Tenter de mettre à jour le projet
        with self.assertRaises(ProjectDBException):
            self.project_repository.update_project(updated_project)

    def test_update_project_duplicate_number(self) -> None:
        """Test de la mise à jour d'un projet avec un numéro déjà utilisé

        Returns:
            None
        """
        # Mettre à jour le premier projet avec le numéro du second
        updated_project = ProjectEntity(
            id=self.project.id,
            project_number=self.second_project.project_number,  # Numéro déjà utilisé par le second projet
            name="Updated Name",
            description="Updated description",
        )

        # Tenter de mettre à jour le projet
        with self.assertRaises(ProjectDBException):
            self.project_repository.update_project(updated_project)

    def test_update_project_with_same_values(self) -> None:
        """Test de la mise à jour d'un projet avec les mêmes valeurs

        Returns:
            None
        """
        # Créer un projet à mettre à jour avec les mêmes valeurs
        same_values_project = ProjectEntity(
            id=self.project.id,
            project_number=self.project.project_number,  # Même numéro de projet
            name=self.project.name,  # Même nom
            description="Description mise à jour",  # Seule la description change
        )

        # Mettre à jour le projet
        result = self.project_repository.update_project(same_values_project)

        # Vérifier que le projet a été mis à jour
        self.assertEqual(same_values_project.id, result.id)
        self.assertEqual(same_values_project.project_number, result.project_number)
        self.assertEqual(same_values_project.name, result.name)
        self.assertEqual(same_values_project.description, result.description)
