import unittest
from typing import ClassVar

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from infra.data.sql_database import SQLDatabase
from infra.web.settings import AppSettings


class DatabaseTests(unittest.TestCase):
    database: ClassVar[SQLDatabase]

    @classmethod
    def setUpClass(cls) -> None:
        app_settings = AppSettings(
            DATABASE_URL="sqlite:///:memory:", DATABASE_ECHO=False
        )
        cls.database = SQLDatabase(settings=app_settings)
        cls.database.create_database()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.engine.dispose()

    def setUp(self) -> None:
        self.session = Session(self.__class__.database.engine)

    def test_database_initialization(self) -> None:
        self.assertEqual(self.database.settings.DATABASE_URL, "sqlite:///:memory:")
        self.assertFalse(self.database.settings.DATABASE_ECHO)
        self.assertIsNotNone(self.database.engine)

    def test_get_session_returns_valid_session(self) -> None:
        with self.database.get_session() as session:
            self.assertIsInstance(session, Session)
            self.assertEqual(session.get_bind(), self.__class__.database.engine)

    def test_get_session_raises_exception_on_error(self) -> None:
        with self.assertRaises(SQLAlchemyError):
            with self.database.get_session():
                raise SQLAlchemyError("Intentional Exception")
