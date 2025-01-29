import unittest
from typing import ClassVar

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from infra.data.database import Database
from infra.web.settings import AppSettings


class TestDatabase(unittest.TestCase):
    database: ClassVar[Database]

    @classmethod
    def setUpClass(cls) -> None:
        settings = AppSettings(DATABASE_URL="sqlite:///:memory:", DATABASE_ECHO=False)
        cls.database = Database(settings=settings)
        cls.database.create_database()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.engine.dispose()

    def setUp(self) -> None:
        self.session = Session(self.__class__.database.engine)

    def test_database_initialization(self) -> None:
        # given when then
        self.assertEqual(self.database.settings.DATABASE_URL, "sqlite:///:memory:")
        self.assertEqual(self.database.settings.DATABASE_ECHO, False)
        self.assertIsNotNone(self.database.engine)

    def test_get_session(self) -> None:
        # given when then
        with self.database.get_session() as session:
            self.assertIsInstance(session, Session)
            self.assertIs(session.get_bind(), self.__class__.database.engine)

    def test_get_session_with_exception(self) -> None:
        # given when then
        with self.assertRaises(SQLAlchemyError):
            with self.database.get_session():
                raise SQLAlchemyError("Test Exception")
