from pydantic_core import ErrorDetails


class UserDBException(Exception):
    """Exception pour les erreurs de base de données

    Args:
        Exception (Exception): Exception de base
    """

    def __init__(self, message: str) -> None:
        super().__init__(f"UserDBException : {message}")


class UserValidationException(Exception):
    """Exception pour les erreurs de validation

    Args:
        Exception (Exception): Exception de base
    """

    def __init__(self, errors: list[ErrorDetails]):
        self.errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in errors
        ]
        super().__init__("UserValidationException")
