from pydantic_core import ErrorDetails


class ProjectException(Exception):
    """Exception de base pour les projets

    Args:
        Exception (Exception): Exception de base
    """

    def __init__(self, message: str = "Exception pour les erreurs de projet") -> None:
        """Initialise l'exception

        Args:
            message (str, optional): Message d'erreur. Defaults to "Exception de projet".
        """
        self.message = message
        super().__init__(f"ProjectException : {message}")


class ProjectDBException(ProjectException):
    """Exception de base de données pour les projets

    Args:
        ProjectException (ProjectException): Exception de base pour les projets
    """

    def __init__(
        self, message: str = "Exception pour les erreurs de base de données"
    ) -> None:
        """Initialise l'exception

        Args:
            message (str, optional): Message d'erreur. Defaults to "Exception de base de données".
        """
        super().__init__(message=message)


class ProjectValidationException(ProjectException):
    """Exception pour la validation d'un projet

    Args:
        ProjectException (ProjectException): Exception de base pour les projets
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
        super().__init__(message="ProjectValidationException")


class ProjectMemberValidationException(ProjectException):
    """Exception pour la validation d'un membre de projet

    Args:
        ProjectException (ProjectException): Exception de base pour les projets
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
        super().__init__(message="ProjectMemberValidationException")
