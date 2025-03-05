from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlmodel import Session


class SQLUnitOfWork:
    """Unit of Work pour la base de données SQL

    Args:
        session_factory (Callable[..., AbstractContextManager[Session]]): Fonction pour créer une session
    """

    def __init__(
        self: "SQLUnitOfWork",
        session_factory: Callable[..., AbstractContextManager[Session]],
    ) -> None:
        """Initialise le unit of work

        Args:
            self (SQLUnitOfWork): Instance du unit of work
            session_factory (Callable[..., AbstractContextManager[Session]]): Fonction pour créer une session
        """
        self.session_factory: Callable[..., AbstractContextManager[Session]] = (
            session_factory
        )
        self.session: Session

    def __enter__(self: "SQLUnitOfWork") -> "SQLUnitOfWork":
        """Entrée du unit of work

        Returns:
            SQLUnitOfWork: Instance du unit of work
        """
        self.session = self.session_factory().__enter__()
        return self

    def __exit__(
        self, exc_type: type | None, exc_val: Exception | None, exc_tb: Exception | None
    ) -> None:
        """Sortie du unit of work

        Args:
            exc_type (type | None): Type de l'exception
            exc_val (Exception | None): Valeur de l'exception
            exc_tb (Exception | None): Traceback de l'exception
        """
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.__exit__(exc_type, exc_val, exc_tb)
