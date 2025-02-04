import unittest
from typing import ClassVar

from infra.data.database import Database
from infra.web.settings import AppSettings


class BaseRepositoryTest(unittest.TestCase):
    database: ClassVar[Database]

    @classmethod
    def setUpClass(cls) -> None:
        app_settings = AppSettings(
            DATABASE_URL="sqlite:///:memory:", DATABASE_ECHO=False
        )
        cls.database = Database(settings=app_settings)
        cls.database.create_database()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.engine.dispose()

    def setUp(self) -> None:
        self.session_context = self.database.get_session()
        self.session = self.session_context.__enter__()

    def tearDown(self) -> None:
        self.session_context.__exit__(None, None, None)
