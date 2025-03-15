from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity, ProjectMemberRole
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
)
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestAddProjectMemberSQLRepository(TestBaseRepository):
    """Test de l'ajout d'un membre à un projet

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur d'ajout d'un membre à un projet

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

        # Créer un utilisateur pour être membre du projet
        self.member = UserEntity(email="member@example.com", password="Password_1234!")
        self.member = self.user_repository.sign_up_user(self.member)

        # Créer un projet valide
        self.valid_project = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project",
            description="A test project",
        )
        self.project = self.project_repository.create_project(
            schema=self.valid_project, creator_id=self.owner.id
        )

    def test_add_project_member_success(self) -> None:
        """Test de l'ajout d'un membre à un projet

        Returns:
            None
        """
        # Ajouter un membre au projet
        project_member = self.project_repository.add_project_member(
            project_id=self.project.id,
            user_id=self.member.id,
            role=ProjectMemberRole.MEMBER,
        )

        # Vérifier que le membre a été ajouté
        self.assertEqual(self.project.id, project_member.project_id)
        self.assertEqual(self.member.id, project_member.user_id)

        # Vérifier que le membre est dans la liste des membres du projet
        project_members = self.project_repository.get_project_members(self.project.id)
        self.assertEqual(2, len(project_members))
        self.assertEqual(self.owner.id, project_members[1].id)
        self.assertEqual(self.member.id, project_members[0].id)

    def test_add_project_member_with_wrong_project_id(self) -> None:
        """Test de l'ajout d'un membre à un projet avec un id de projet invalide

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            wrong_id: UUID = uuid4()
            self.project_repository.add_project_member(
                project_id=wrong_id,
                user_id=self.member.id,
                role=ProjectMemberRole.MEMBER,
            )

        expected_message = (
            f"ProjectException : Le projet avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_add_project_member_with_wrong_user_id(self) -> None:
        """Test de l'ajout d'un membre à un projet avec un id d'utilisateur invalide

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            wrong_id: UUID = uuid4()
            self.project_repository.add_project_member(
                project_id=self.project.id,
                user_id=wrong_id,
                role=ProjectMemberRole.MEMBER,
            )

        expected_message = (
            f"ProjectException : L'utilisateur avec l'id '{wrong_id}' n'existe pas."
        )
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_add_project_member_duplicate_member(self) -> None:
        """Test de l'ajout d'un membre déjà présent dans le projet

        Returns:
            None
        """
        # Ajouter un membre au projet
        self.project_repository.add_project_member(
            project_id=self.project.id,
            user_id=self.member.id,
            role=ProjectMemberRole.MEMBER,
        )

        # Tenter d'ajouter le même membre à nouveau
        with self.assertRaises(ProjectDBException) as context:
            self.project_repository.add_project_member(
                project_id=self.project.id,
                user_id=self.member.id,
                role=ProjectMemberRole.MEMBER,
            )

        expected_message = "ProjectException : L'utilisateur est déjà membre du projet."
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)
