import bcrypt

from users.domain.services.password_hasher_interface import PasswordHasherInterface


class BcryptPasswordHasher(PasswordHasherInterface):
    """Hacheur de mot de passe avec bcrypt

    Args:
        PasswordHasherInterface (PasswordHasherInterface): Interface pour le hachage des mots de passe
    """

    def hash(self, password: str) -> str:
        """Hache un mot de passe

        Args:
            password (str): Mot de passe à hacher

        Returns:
            str: Mot de passe haché
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        """Vérifie un mot de passe

        Args:
            password (str): Mot de passe à vérifier
            hashed (str): Mot de passe haché

        Returns:
            bool: True si le mot de passe est correct, False sinon
        """
        return bcrypt.checkpw(password.encode(), hashed.encode())
