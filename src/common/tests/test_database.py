import os
import unittest
from typing import ClassVar

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from common.infra.data.sql_database import SQLDatabase
from common.infra.web.settings import AppSettings


class TestDatabase(unittest.TestCase):
    """Test de base pour les tests de la base de données

    Args:
        unittest (unittest.TestCase): Testeur de base pour les tests de la base de données
    """

    TEST_DB_PATH: ClassVar[str] = "test.db"
    app_settings: ClassVar[AppSettings]
    database: ClassVar[SQLDatabase]

    @classmethod
    def setUpClass(cls: type["TestDatabase"]) -> None:
        """Initialise la base de données pour tous les tests."""
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)

        cls.app_settings = AppSettings(
            DATABASE_URL=f"sqlite:///{cls.TEST_DB_PATH}", DATABASE_ECHO=False
        )
        cls.database = SQLDatabase(settings=cls.app_settings)
        cls.database.create_database()

    def setUp(self: "TestDatabase") -> None:
        """Ouvre une session avant chaque test."""
        self.session_context = self.database.get_session()
        self.session = self.session_context.__enter__()

    def tearDown(self: "TestDatabase") -> None:
        """Ferme la session et nettoie la base après chaque test."""
        self.session_context.__exit__(None, None, None)

    @classmethod
    def tearDownClass(cls: type["TestDatabase"]) -> None:
        """Supprime la base après les tests."""
        cls.database.engine.dispose()
        if os.path.exists(cls.TEST_DB_PATH):
            os.remove(cls.TEST_DB_PATH)

    def test_database_initialization(self: "TestDatabase") -> None:
        """Test de l'initialisation de la base de données."""
        self.assertEqual(self.database.settings.DATABASE_URL, "sqlite:///test.db")
        self.assertFalse(self.database.settings.DATABASE_ECHO)
        self.assertIsNotNone(self.database.engine)

    def test_get_session_returns_valid_session(self: "TestDatabase") -> None:
        """Test de la récupération d'une session valide."""
        with self.database.get_session() as session:
            self.assertIsInstance(session, Session)
            self.assertEqual(session.get_bind(), self.__class__.database.engine)

    def test_get_session_raises_exception_on_error(self: "TestDatabase") -> None:
        """Test de l'exception levée lors d'une erreur."""
        with self.assertRaises(SQLAlchemyError):
            with self.database.get_session():
                raise SQLAlchemyError("Intentional Exception")
