import unittest
from typing import ClassVar

from infra.data.sql_database import SQLDatabase
from infra.data.sql_unit_of_work import SQLUnitOfWork
from infra.web.settings import AppSettings


class BaseRepositoryTest(unittest.TestCase):
    database: ClassVar[SQLDatabase]
    uow: ClassVar[SQLUnitOfWork]

    @classmethod
    def setUpClass(cls) -> None:
        app_settings = AppSettings(
            DATABASE_URL="sqlite:///:memory:", DATABASE_ECHO=False
        )
        cls.database = SQLDatabase(settings=app_settings)
        cls.database.create_database()
        cls.uow = SQLUnitOfWork(session_factory=cls.database.get_session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.engine.dispose()

    def setUp(self) -> None:
        self.session_context = self.database.get_session()
        self.session = self.session_context.__enter__()

    def tearDown(self) -> None:
        self.session_context.__exit__(None, None, None)
