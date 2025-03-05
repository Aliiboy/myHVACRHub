from abc import ABC, abstractmethod


class PasswordHasherInterface(ABC):
    """Interface pour le hachage des mots de passe

    Cette interface définit les méthodes nécessaires pour hacher et vérifier
    les mots de passe.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hache un mot de passe

        Args:
            password (str): Mot de passe à hacher

        Returns:
            str: Mot de passe haché
        """
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        """Vérifie un mot de passe

        Args:
            password (str): Mot de passe à vérifier
            hashed (str): Mot de passe haché

        Returns:
            bool: True si le mot de passe est correct, False sinon
        """
        pass
