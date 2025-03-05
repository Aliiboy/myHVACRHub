from abc import ABC, abstractmethod
from uuid import UUID

from users.domain.entities.user_entity import UserEntity


class UserRepositoryInterface(ABC):
    """Interface pour les opérations de base de données sur les utilisateurs"""

    # write
    @abstractmethod
    def sign_up_user(self, schema: UserEntity) -> UserEntity:
        """Enregistre un nouvel utilisateur

        Args:
            schema (UserEntity): Schéma de l'utilisateur à enregistrer

        Returns:
            UserEntity: Utilisateur enregistré
        """
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: UUID) -> None:
        """Supprime un utilisateur par son identifiant

        Args:
            user_id (UUID): Identifiant de l'utilisateur à supprimer
        """
        pass

    # read
    @abstractmethod
    def login_user(self, schema: UserEntity) -> UserEntity:
        """Connecte un utilisateur

        Args:
            schema (UserEntity): Schéma de l'utilisateur à connecter

        Returns:
            UserEntity: Utilisateur connecté
        """
        pass

    @abstractmethod
    def get_user_profile(self, user_id: UUID) -> UserEntity:
        """Récupère le profil d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur à récupérer

        Returns:
            UserEntity: Utilisateur récupéré
        """
        pass

    @abstractmethod
    def get_all_users_with_limit(self, limit: int) -> list[UserEntity]:
        """Récupère tous les utilisateurs avec une limite

        Args:
            limit (int): Limite de récupération

        Returns:
            list[UserEntity]: Liste des utilisateurs récupérés
        """
        pass
