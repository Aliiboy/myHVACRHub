import os
import unittest
from typing import ClassVar

from sqlalchemy import text

from common.infra.data.sql_database import SQLDatabase
from common.infra.data.sql_unit_of_work import SQLUnitOfWork
from common.infra.web.settings import AppSettings
from users.infra.services.bcrypt_password_hasher import BcryptPasswordHasher


class TestBaseRepository(unittest.TestCase):
    """Test de base pour les tests des repositories

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des repositories
    """

    TEST_DB_PATH: ClassVar[str] = "test.db"
    app_settings: ClassVar[AppSettings]
    database: ClassVar[SQLDatabase]

    @classmethod
    def setUpClass(cls) -> None:
        """Initialise une base persistante pour tous les tests."""
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)

        cls.app_settings = AppSettings(
            DATABASE_URL=f"sqlite:///{cls.TEST_DB_PATH}", DATABASE_ECHO=False
        )
        cls.database = SQLDatabase(settings=cls.app_settings)
        cls.database.create_database()

    def setUp(self) -> None:
        """Initialise une base persistante pour tous les tests."""
        self.uow = SQLUnitOfWork(session_factory=self.database.get_session)
        self.password_hasher = BcryptPasswordHasher()
        self.session_context = self.database.get_session()
        self.session = self.session_context.__enter__()

    def tearDown(self) -> None:
        """Ferme la session et nettoie la base après chaque test."""
        self.session_context.__exit__(None, None, None)
        with self.database.get_session() as session:
            session.execute(text("DELETE FROM project_members_links"))
            session.execute(text("DELETE FROM projects"))
            session.execute(text("DELETE FROM users"))
            session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        """Nettoie la base après les tests."""
        cls.database.engine.dispose()
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)
