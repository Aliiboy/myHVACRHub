from abc import ABC, abstractmethod
from uuid import UUID

from users.domain.entities.user_entity import UserRole


class TokenServiceInterface(ABC):
    """Interface pour le service de génération de jetons

    Cette interface définit les méthodes nécessaires pour générer un jeton
    pour un utilisateur.
    """

    @abstractmethod
    def generate_token(self, user_id: UUID, role: UserRole) -> str:
        """Génère un jeton pour un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur
            role (UserRole): Rôle de l'utilisateur

        Returns:
            str: Jeton généré
        """
        pass
