from uuid import UUID, uuid4

from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity, ProjectMemberRole
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestGetUserProjectsSQLRepository(TestBaseRepository):
    """Test de la récupération des projets d'un utilisateur

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de récupération des projets d'un utilisateur

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

        # Créer plusieurs projets
        self.project1 = ProjectEntity(
            project_number="PRJ-001",
            name="Test Project 1",
            description="A test project 1",
        )
        self.project1 = self.project_repository.create_project(
            schema=self.project1, creator_id=self.user1.id
        )

        self.project2 = ProjectEntity(
            project_number="PRJ-002",
            name="Test Project 2",
            description="A test project 2",
        )
        self.project2 = self.project_repository.create_project(
            schema=self.project2, creator_id=self.user2.id
        )

        self.project3 = ProjectEntity(
            project_number="PRJ-003",
            name="Test Project 3",
            description="A test project 3",
        )
        self.project3 = self.project_repository.create_project(
            schema=self.project3, creator_id=self.user2.id
        )

        # Ajouter des membres aux projets
        self.project_repository.add_project_member(
            project_id=self.project2.id,
            user_id=self.user1.id,
            role=ProjectMemberRole.MEMBER,
        )

    def test_get_user_projects_success(self) -> None:
        """Test de la récupération des projets d'un utilisateur avec succès

        Returns:
            None
        """
        # Récupérer les projets de user1
        user1_projects = self.project_repository.get_user_projects(self.user1.id)

        # Vérifier que user1 est membre de project1 et project2
        self.assertEqual(2, len(user1_projects))
        project_ids = [project.id for project in user1_projects]
        self.assertIn(self.project1.id, project_ids)
        self.assertIn(self.project2.id, project_ids)
        self.assertNotIn(self.project3.id, project_ids)

        # Récupérer les projets de user2
        user2_projects = self.project_repository.get_user_projects(self.user2.id)

        # Vérifier que user2 est membre de project2 et project3
        self.assertEqual(2, len(user2_projects))
        project_ids = [project.id for project in user2_projects]
        self.assertIn(self.project2.id, project_ids)
        self.assertIn(self.project3.id, project_ids)
        self.assertNotIn(self.project1.id, project_ids)

    def test_get_user_projects_user_without_projects(self) -> None:
        """Test de la récupération des projets d'un utilisateur qui n'est membre d'aucun projet

        Returns:
            None
        """
        # Créer un utilisateur sans projet
        user_without_projects = UserEntity(
            email="no_projects@example.com", password="Password_1234!"
        )
        user_without_projects = self.user_repository.sign_up_user(user_without_projects)

        # Récupérer les projets de l'utilisateur
        projects = self.project_repository.get_user_projects(user_without_projects.id)

        # Vérifier que l'utilisateur n'est membre d'aucun projet
        self.assertEqual(0, len(projects))

    def test_get_user_projects_nonexistent_user(self) -> None:
        """Test de la récupération des projets d'un utilisateur qui n'existe pas

        Returns:
            None
        """
        # Récupérer les projets d'un utilisateur qui n'existe pas
        non_existent_user_id: UUID = uuid4()
        projects = self.project_repository.get_user_projects(non_existent_user_id)

        # Vérifier que la liste est vide
        self.assertEqual(0, len(projects))
