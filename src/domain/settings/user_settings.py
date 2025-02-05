class UserSettings:
    # id
    id_description: str = "Identifiant unique de l'utilisateur"
    # email
    email_description: str = "Adresse email unique de l'utilisateur"
    # password
    password_description: str = (
        "Mot de passe contenant au moins un chiffre et un caractère spécial"
    )
    password_min_length: int = 6
    password_pattern: str = (
        r"[A-Za-z\d@$!%*?&]*\d+[A-Za-z\d@$!%*?&]*[@$!%*?&]+[A-Za-z\d@$!%*?&]*"
    )
    # token
    access_token_description: str = "Token JWT pour l'authentification"
    token_type_description: str = "Type de token"
    # date
    created_at_description: str = (
        "Date a laquelle l'utilisateur est rentré dans la base de données"
    )
