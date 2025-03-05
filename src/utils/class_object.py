from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def singleton(cls: Callable[..., T]) -> Callable[..., T]:
    """Décorateur pour rendre une classe singleton

    Args:
        cls (Callable[..., T]): Classe à décorer

    Returns:
        Callable[..., T]: Classe décorée
    """
    instances: dict[Any, T] = {}

    def wrapper(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
