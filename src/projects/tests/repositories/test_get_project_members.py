from uuid import UUID, uuid4

from common.tests.repositories.base_repo_test import BaseRepositoryTest
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import ProjectDBException
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class GetProjectMembersSQLRepositoryTests(BaseRepositoryTest):
    """Test de la récupération des membres d'un projet

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de récupération des membres d'un projet

        Returns:
            None
        """
        super().setUp()
        self.project_repository = ProjectSQLRepository(unit_of_work=self.uow)
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )

        # Créer des utilisateurs pour le test
        self.user1 = UserEntity(email="user1@example.com", password="Password_1234!")
        self.user1 = self.user_repository.sign_up_user(self.user1)

        self.user2 = UserEntity(email="user2@example.com", password="Password_1234!")
        self.user2 = self.user_repository.sign_up_user(self.user2)

        # Créer un projet
        self.project = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project",
            description="A test project",
        )
        self.project = self.project_repository.create_project(self.project)

        # Ajouter des membres au projet
        self.project_repository.add_project_member(
            project_id=self.project.id,
            user_id=self.user1.id,
        )
        self.project_repository.add_project_member(
            project_id=self.project.id,
            user_id=self.user2.id,
        )

    def test_get_project_members_success(self) -> None:
        """Test de la récupération des membres d'un projet avec succès

        Returns:
            None
        """
        # Récupérer les membres du projet
        members = self.project_repository.get_project_members(self.project.id)

        # Vérifier que les membres ont été récupérés
        self.assertEqual(2, len(members))
        member_ids = [member.id for member in members]
        self.assertIn(self.user1.id, member_ids)
        self.assertIn(self.user2.id, member_ids)

    def test_get_project_members_project_not_found(self) -> None:
        """Test de la récupération des membres d'un projet qui n'existe pas

        Returns:
            None
        """
        with self.assertRaises(ProjectDBException) as context:
            non_existent_project_id: UUID = uuid4()
            self.project_repository.get_project_members(non_existent_project_id)

        expected_message = f"ProjectException : Le projet avec l'id '{non_existent_project_id}' n'existe pas."
        self.assertIsInstance(context.exception, ProjectDBException)
        self.assertEqual(str(context.exception), expected_message)

    def test_get_project_members_empty(self) -> None:
        """Test de la récupération des membres d'un projet vide

        Returns:
            None
        """
        # Créer un projet sans membre
        empty_project = ProjectEntity(
            project_number="PRJ-002",
            name="Empty Project",
            description="A project without members",
        )
        empty_project = self.project_repository.create_project(empty_project)

        # Récupérer les membres du projet
        members = self.project_repository.get_project_members(empty_project.id)

        # Vérifier que la liste est vide
        self.assertEqual(0, len(members))
