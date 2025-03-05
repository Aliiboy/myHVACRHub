from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import QueuePool
from sqlmodel import Session, SQLModel, create_engine

from common.infra.web.settings import AppSettings
from utils.class_object import singleton


@singleton
class SQLDatabase:
    """Base de données SQL

    Args:
        settings (AppSettings): Paramètres de l'application
    """

    def __init__(self: "SQLDatabase", settings: AppSettings) -> None:
        """Initialise la base de données SQL

        Args:
            self (SQLDatabase): Instance de la base de données SQL
            settings (AppSettings): Paramètres de l'application
        """
        self.settings = settings
        self.engine = create_engine(
            self.settings.DATABASE_URL,
            echo=self.settings.DATABASE_ECHO,
            poolclass=QueuePool,
            pool_size=self.settings.DATABASE_POOL_SIZE,
        )

    def create_database(self: "SQLDatabase") -> None:
        """Crée la base de données SQL

        Args:
            self (SQLDatabase): Instance de la base de données SQL
        """
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self: "SQLDatabase") -> Iterator[Session]:
        """Obtient une session de la base de données SQL

        Args:
            self (SQLDatabase): Instance de la base de données SQL

        Returns:
            Iterator[Session]: Session de la base de données SQL
        """
        session = Session(self.engine)
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
