from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def singleton(cls: Callable[..., T]) -> Callable[..., T]:
    instances: dict[Any, T] = {}

    def wrapper(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
