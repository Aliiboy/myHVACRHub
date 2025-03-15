class UserSettings:
    """Paramètres de l'utilisateur

    Cette classe contient les paramètres de l'utilisateur.
    """

    # user_id
    user_id_description: str = "Identifiant unique de l'utilisateur"
    # email
    email_description: str = "Adresse email unique de l'utilisateur"
    # password
    password_description: str = "Mot de passe contenant au moins 6 caractères, un chiffre et un caractère spécial"
    password_min_length: int = 6
    password_pattern: str = (
        r"[A-Za-z\d@$!%*?&]*\d+[A-Za-z\d@$!%*?&]*[@$!%*?&]+[A-Za-z\d@$!%*?&]*"
    )
    # role
    role_description: str = "Niveau de permission de l'utilisateur"
    # token
    access_token_description: str = "Token JWT pour l'authentification"
    token_type_description: str = "Type de token"
    # date
    created_at_description: str = (
        "Date a laquelle l'utilisateur est rentré dans la base de données"
    )
    updated_at_description: str = (
        "Date a laquelle l'utilisateur a été modifié dans la base de données"
    )
    # limit
    limit_description: str = "Nombre maximum d'utilisateurs à récupérer"
    limit_default: int = 100
    limit_gt: int = 0
    # users
    users_description: str = "Liste des utilisateurs"
