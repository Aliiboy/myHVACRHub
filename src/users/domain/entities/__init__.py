from users.domain.entities.user_entity import UserEntity


# Mise à jour du schéma de modèle après l'importation de tous les modules
# pour résoudre les références avancées
def update_forward_refs() -> None:
    from projects.domain.entities.project_entity import ProjectEntity

    UserEntity.model_rebuild()
    ProjectEntity.model_rebuild()


update_forward_refs()
