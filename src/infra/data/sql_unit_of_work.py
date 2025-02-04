from collections.abc import Callable
from contextlib import AbstractContextManager

from sqlmodel import Session


class SQLUnitOfWork:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory: Callable[..., AbstractContextManager[Session]] = (
            session_factory
        )
        self.session: Session

    def __enter__(self) -> "SQLUnitOfWork":
        self.session = self.session_factory().__enter__()
        return self

    def __exit__(
        self, exc_type: type | None, exc_val: Exception | None, exc_tb: Exception | None
    ) -> None:
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.__exit__(exc_type, exc_val, exc_tb)
