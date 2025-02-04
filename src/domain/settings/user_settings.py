class UserSettings:
    # id
    id_description: str = "Identifiant unique de l'utilisateur"
    # email
    email_description: str = "Adresse email unique de l'utilisateur"
    # password
    password_description: str = "Mot de passe sécurisé de l'utilisateur"
    password_min_length: int = 8
    password_max_length: int = 128
    # token
    access_token_description: str = "Token JWT pour l'authentification"
    token_type_description: str = "Type de token"
    # date
    created_at_description: str = (
        "Date a laquelle l'utilisateur est rentré dans la base de données"
    )
