from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestGetAllProjectsWithLimitSQLRepository(TestBaseRepository):
    """Test de la récupération de tous les projets avec une limite

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de récupération de tous les projets avec une limite

        Returns:
            None
        """
        super().setUp()
        self.project_repository = ProjectSQLRepository(unit_of_work=self.uow)
        self.user_repository = UserSQLRepository(
            unit_of_work=self.uow, password_hasher=self.password_hasher
        )

        # Créer un utilisateur pour être propriétaire des projets
        self.valid_user = UserEntity(
            email="owner@example.com", password="Password_1234!"
        )
        self.user = self.user_repository.sign_up_user(self.valid_user)

        # Créer plusieurs projets
        self.projects = []
        for i in range(5):
            project = ProjectEntity(
                project_number=f"PRJ-{i + 1:03d}",
                name=f"Test Project {i + 1}",
                description=f"A test project {i + 1}",
            )
            created_project = self.project_repository.create_project(
                schema=project, creator_id=self.user.id
            )
            self.projects.append(created_project)

    def test_get_all_projects_with_limit_success(self) -> None:
        """Test de la récupération de tous les projets avec une limite

        Returns:
            None
        """
        # Récupérer tous les projets avec une limite de 3
        projects = self.project_repository.get_all_projects_with_limit(3)

        # Vérifier que la limite est respectée
        self.assertEqual(3, len(projects))

        # Récupérer tous les projets avec une limite de 10 (plus que le nombre total)
        all_projects = self.project_repository.get_all_projects_with_limit(10)

        # Vérifier que tous les projets sont récupérés
        self.assertEqual(5, len(all_projects))

    def test_get_all_projects_with_limit_zero(self) -> None:
        """Test de la récupération de tous les projets avec une limite de zéro

        Returns:
            None
        """
        # Récupérer tous les projets avec une limite de 0
        projects = self.project_repository.get_all_projects_with_limit(0)

        # Vérifier qu'aucun projet n'est récupéré
        self.assertEqual(0, len(projects))

    def test_get_all_projects_with_limit_empty_db(self) -> None:
        """Test de la récupération de tous les projets avec une limite quand la base de données est vide

        Returns:
            None
        """
        # Supprimer tous les projets
        for project in self.projects:
            self.project_repository.delete_project_by_id(project.id)

        # Récupérer tous les projets avec une limite de 10
        projects = self.project_repository.get_all_projects_with_limit(10)

        # Vérifier qu'aucun projet n'est récupéré
        self.assertEqual(0, len(projects))
