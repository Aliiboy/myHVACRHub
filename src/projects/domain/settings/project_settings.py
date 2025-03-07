class ProjectSettings:
    """Paramètres du projet

    Cette classe contient les paramètres des projets.
    """

    # id
    id_description: str = "Identifiant unique du projet"
    # project_number
    project_number_description: str = (
        "Numéro de projet utilisé comme identifiant par l'entreprise"
    )
    project_number_max_length: int = 250
    # name
    name_description: str = "Nom du projet"
    name_max_length: int = 250
    # description
    description_description: str = "Description du projet"
    description_max_length: int = 250
    # owner
    owner_id_description: str = "Identifiant unique du propriétaire du projet"
    owner_description: str = "L'entité propriétaire du projet"
    # members
    members_description: str = "Liste des membres du projet"
    # dates
    created_at_description: str = "Date de création du projet"
    updated_at_description: str = "Date de mise à jour du projet"
    # ProjectMemberRole
    role_description: str = "Rôle de l'utilisateur dans le projet"
