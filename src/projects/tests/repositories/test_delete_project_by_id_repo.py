from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
)
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestDeleteProjectByIdSQLRepository(TestBaseRepository):
    """Test de la suppression d'un projet par son identifiant

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de suppression d'un projet par son identifiant

        Returns:
            None
        """
        super().setUp()
        self.project_repository = ProjectSQLRepository(unit_of_work=self.uow)
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )

        # Créer un utilisateur pour être propriétaire du projet
        self.valid_user = UserEntity(
            email="owner@example.com", password="Password_1234!"
        )
        self.user = self.user_repository.sign_up_user(self.valid_user)

        # Créer un projet valide
        self.valid_project = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project",
            description="A test project",
        )
        self.project = self.project_repository.create_project(
            schema=self.valid_project, creator_id=self.user.id
        )

    def test_delete_project_by_id_success(self) -> None:
        """Test de la suppression d'un projet par son identifiant

        Returns:
            None
        """
        # Vérifier que le projet existe avant la suppression
        retrieved_project = self.project_repository.get_project_by_id(self.project.id)
        self.assertEqual(self.project.id, retrieved_project.id)

        # Supprimer le projet
        self.project_repository.delete_project_by_id(self.project.id)

        # Vérifier que le projet n'existe plus
        with self.assertRaises(ProjectDBException):
            self.project_repository.get_project_by_id(self.project.id)

    def test_delete_project_by_id_with_wrong_id(self) -> None:
        """Test de la suppression d'un projet avec un id invalide

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            wrong_id: UUID = uuid4()
            self.project_repository.delete_project_by_id(wrong_id)

        expected_message = (
            f"ProjectException : Le projet avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)
