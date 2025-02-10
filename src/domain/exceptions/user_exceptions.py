class UserAlreadyExistsException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"L'email '{email}' est déjà utilisé.")


class UserNotFoundException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"L'utilisateur avec l'email '{email}' n'existe pas.")


class UserInvalidPasswordException(Exception):
    def __init__(self) -> None:
        super().__init__("Mot de passe incorrect.")


class UserInvalidPasswordPatternException(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Le mot de passe doit contenir au moins 6 caractères, un chiffre et un caractère spécial."
        )
