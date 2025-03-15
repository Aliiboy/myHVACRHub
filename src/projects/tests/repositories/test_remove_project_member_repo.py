from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity, ProjectMemberRole
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
)
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestDeleteProjectMemberSQLRepository(TestBaseRepository):
    """Test de la suppression d'un membre d'un projet

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de suppression d'un membre d'un projet

        Returns:
            None
        """
        super().setUp()
        self.project_repository = ProjectSQLRepository(unit_of_work=self.uow)
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )

        # Créer des utilisateurs pour le test
        self.owner = UserEntity(email="owner@example.com", password="Password_1234!")
        self.owner = self.user_repository.sign_up_user(self.owner)

        self.member = UserEntity(email="member@example.com", password="Password_1234!")
        self.member = self.user_repository.sign_up_user(self.member)

        self.another_member = UserEntity(
            email="another@example.com", password="Password_1234!"
        )
        self.another_member = self.user_repository.sign_up_user(self.another_member)

        # Créer un projet valide
        self.valid_project = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project",
            description="A test project",
        )
        self.project = self.project_repository.create_project(
            schema=self.valid_project, creator_id=self.owner.id
        )

        # Ajouter un membre au projet
        self.project_repository.add_project_member(
            project_id=self.project.id,
            user_id=self.member.id,
            role=ProjectMemberRole.MEMBER,
        )

    def test_delete_project_member_success(self) -> None:
        """Test de la suppression d'un membre d'un projet avec succès

        Returns:
            None
        """
        # Vérifier que le membre est bien dans le projet
        project_members = self.project_repository.get_project_members(self.project.id)
        self.assertEqual(2, len(project_members))
        self.assertEqual(self.owner.id, project_members[1].id)
        self.assertEqual(self.member.id, project_members[0].id)

        # Supprimer le membre du projet
        self.project_repository.delete_project_member(
            project_id=self.project.id,
            user_id=self.member.id,
        )

        # Vérifier que le membre a été supprimé
        project_members = self.project_repository.get_project_members(self.project.id)
        self.assertEqual(1, len(project_members))

    def test_delete_project_member_project_not_found(self) -> None:
        """Test de la suppression d'un membre d'un projet qui n'existe pas

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            non_existent_project_id: UUID = uuid4()
            self.project_repository.delete_project_member(
                project_id=non_existent_project_id,
                user_id=self.member.id,
            )

        expected_message = f"ProjectException : Le projet avec l'id '{non_existent_project_id}' n'existe pas."
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_delete_project_member_not_a_member(self) -> None:
        """Test de la suppression d'un utilisateur qui n'est pas membre du projet

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            self.project_repository.delete_project_member(
                project_id=self.project.id,
                user_id=self.another_member.id,  # Cet utilisateur n'est pas membre du projet
            )

        expected_message = (
            "ProjectException : L'utilisateur n'est pas membre du projet."
        )
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_delete_project_member_user_not_found(self) -> None:
        """Test de la suppression d'un utilisateur qui n'existe pas

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            non_existent_user_id: UUID = uuid4()
            self.project_repository.delete_project_member(
                project_id=self.project.id,
                user_id=non_existent_user_id,
            )

        expected_message = (
            "ProjectException : L'utilisateur n'est pas membre du projet."
        )
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)
