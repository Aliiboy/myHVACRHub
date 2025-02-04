from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import QueuePool
from sqlmodel import Session, SQLModel, create_engine

from infra.web.settings import AppSettings
from utils.class_object import singleton


@singleton
class SQLDatabase:
    def __init__(self: "SQLDatabase", settings: AppSettings) -> None:
        self.settings = settings
        self.engine = create_engine(
            self.settings.DATABASE_URL,
            echo=self.settings.DATABASE_ECHO,
            poolclass=QueuePool,
            pool_size=self.settings.DATABASE_POOL_SIZE,
        )

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self: "SQLDatabase") -> Iterator[Session]:
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
