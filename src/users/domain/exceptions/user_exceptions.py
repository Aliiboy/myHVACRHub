from pydantic_core import ErrorDetails


class UserException(Exception):
    """Exception pour les erreurs de l'utilisateur

    Args:
        Exception (Exception): Exception de base
    """

    def __init__(
        self, message: str = "Exception pour les erreurs de l'utilisateur"
    ) -> None:
        """Initialise l'exception

        Args:
            message (str, optional): Message d'erreur. Defaults to "Exception pour les erreurs de l'utilisateur".
        """
        self.message = message
        super().__init__(f"UserException : {message}")


class UserDBException(UserException):
    """Exception pour les erreurs de base de données

    Args:
        UserException (UserException): Exception de base
    """

    def __init__(
        self, message: str = "Exception pour les erreurs de base de données"
    ) -> None:
        """Initialise l'exception

        Args:
            message (str, optional): Message d'erreur. Defaults to "Exception pour les erreurs de base de données".
        """
        super().__init__(message=message)


class UserValidationException(UserException):
    """Exception pour les erreurs de validation d'un utilisateur

    Args:
        UserException (UserException): Exception de base
    """

    def __init__(self, errors: list[ErrorDetails]):
        """Initialise l'exception

        Args:
            errors (list[ErrorDetails]): Liste des erreurs de validation
        """
        self.errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in errors
        ]
        super().__init__(message="UserValidationException")
