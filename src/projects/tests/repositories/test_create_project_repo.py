from common.tests.repositories.test_base_repo import TestBaseRepository
from projects.domain.entities.project_entity import ProjectEntity
from projects.domain.exceptions.project_exceptions import ProjectDBException
from projects.infra.data.repositories.project_sqlrepo import ProjectSQLRepository
from users.domain.entities.user_entity import UserEntity
from users.infra.data.repositories.user_sqlrepo import UserSQLRepository


class TestCreateProjectSQLRepository(TestBaseRepository):
    """Test de la création d'un projet

    Args:
        BaseRepositoryTest (BaseRepositoryTest): Testeur de base pour les tests des répositories
    """

    def setUp(self) -> None:
        """Initialise le testeur de création d'un projet

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

    def test_create_project_success(self) -> None:
        """Test de la création d'un projet

        Returns:
            None
        """
        # Utiliser un projet avec un nom unique pour ce test
        test_project = ProjectEntity(
            project_number="PRJ-S01",
            name="Test Project Success",
            description="A test project for success",
        )

        created_project = self.project_repository.create_project(
            schema=test_project, creator_id=self.user.id
        )

        self.assertEqual(test_project.project_number, created_project.project_number)
        self.assertEqual(test_project.name, created_project.name)
        self.assertEqual(test_project.description, created_project.description)

    def test_create_project_duplicate_project_number_raises_exception(self) -> None:
        """Test de la création d'un projet avec un numéro de projet déjà utilisé

        Returns:
            None
        """
        # D'abord, créer un premier projet
        first_project = ProjectEntity(
            project_number="PRJ-D01",
            name="Test Project Duplicate Number 1",
            description="A test project for duplicate number",
        )
        self.project_repository.create_project(
            schema=first_project, creator_id=self.user.id
        )

        # Ensuite, tenter de créer un projet avec le même numéro
        duplicate_project = ProjectEntity(
            project_number="PRJ-D01",  # Même numéro de projet
            name="Test Project Duplicate Number 2",  # Nom différent
            description="A different project",
        )

        with self.assertRaises(ProjectDBException):
            self.project_repository.create_project(
                schema=duplicate_project, creator_id=self.user.id
            )

    def test_create_project_duplicate_name_raises_exception(self) -> None:
        """Test de la création d'un projet avec un nom déjà utilisé

        Returns:
            None
        """
        # D'abord, créer un premier projet
        first_project = ProjectEntity(
            project_number="PRJ-N01",
            name="Test Project Duplicate Name",
            description="A test project for duplicate name",
        )
        self.project_repository.create_project(
            schema=first_project, creator_id=self.user.id
        )

        # Ensuite, tenter de créer un projet avec le même nom
        duplicate_project = ProjectEntity(
            project_number="PRJ-N02",  # Numéro de projet différent
            name="Test Project Duplicate Name",  # Même nom
            description="A different project",
        )

        with self.assertRaises(ProjectDBException):
            self.project_repository.create_project(
                schema=duplicate_project, creator_id=self.user.id
            )
