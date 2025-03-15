import os
import unittest
from typing import ClassVar

from sqlalchemy import text

from common.infra.data.sql_database import SQLDatabase
from common.infra.web.app import WebApp
from common.infra.web.container import AppContainer
from common.infra.web.settings import AppSettings


class TestBaseAPI(unittest.TestCase):
    """Test de base pour les tests des API

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests des API
    """

    TEST_DB_PATH: ClassVar[str] = "test.db"
    app_settings: ClassVar[AppSettings]
    container: ClassVar[AppContainer]
    database: ClassVar[SQLDatabase]
    web_app_instance: ClassVar[WebApp]
    web_application: ClassVar
    client: ClassVar

    @classmethod
    def setUpClass(cls) -> None:
        """Initialise une base de test persistante."""
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)

        cls.app_settings = AppSettings(
            DATABASE_URL=f"sqlite:///{cls.TEST_DB_PATH}", DATABASE_ECHO=False
        )
        cls.container = AppContainer()
        cls.container.app_settings.override(cls.app_settings)

        cls.database = cls.container.database()
        cls.database.create_database()

        cls.web_app_instance = WebApp(container=cls.container)
        cls.web_application = cls.web_app_instance.app
        cls.client = cls.web_application.test_client()

    def setUp(self) -> None:
        """Ouvre une session avant chaque test."""
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
        """Supprime la base après les tests."""
        cls.database.engine.dispose()
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)
