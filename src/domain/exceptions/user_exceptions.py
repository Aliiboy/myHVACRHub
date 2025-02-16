from pydantic_core import ErrorDetails


class UserNotFoundException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"L'utilisateur avec l'email '{email}' n'existe pas.")


class UserInvalidPasswordException(Exception):
    def __init__(self) -> None:
        super().__init__("Mot de passe incorrect.")


class UserDBException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"UserDBException : {message}")


class UserValidationException(Exception):
    def __init__(self, errors: list[ErrorDetails]):
        self.errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in errors
        ]
        super().__init__("UserValidationException")
