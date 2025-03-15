from uuid import UUID

from pydantic import BaseModel


class ProjectCreateSchema(BaseModel):
    """Schéma pour la création d'un projet

    Ce schéma définit les données requises pour créer un nouveau projet.

    Attributs:
        project_number (str): Numéro du projet
        name (str): Nom du projet
        description (str): Description du projet
    """

    project_number: str
    name: str
    description: str


class ProjectUpdateSchema(BaseModel):
    """Schéma pour la mise à jour d'un projet

    Ce schéma définit les données requises pour mettre à jour un projet existant.

    Attributs:
        id (UUID): Identifiant unique pour le projet
        project_number (str): Numéro du projet
        name (str): Nom du projet
        description (str): Description du projet
    """

    id: UUID
    project_number: str
    name: str
    description: str


class ProjectAddMemberSchema(BaseModel):
    """Schéma pour l'ajout d'un membre à un projet

    Ce schéma définit les données requises pour ajouter un membre à un projet.

    Attributs:
        project_id (UUID): ID du projet
        user_id (UUID): ID de l'utilisateur à ajouter au projet
        role (ProjectMemberRole): Rôle de l'utilisateur dans le projet
    """

    project_id: UUID
    user_id: UUID
