from uuid import UUID

from sqlmodel import asc, select

from common.infra.data.sql_unit_of_work import SQLUnitOfWork
from users.app.repositories.user_interface import UserRepositoryInterface
from users.domain.entities.user_entity import UserEntity
from users.domain.exceptions.user_exceptions import (
    UserDBException,
)
from users.domain.services.password_hasher_interface import PasswordHasherInterface
from users.infra.data.models.user_sqlmodel import UserSQLModel


class UserSQLRepository(UserRepositoryInterface):
    """Repository pour les utilisateurs

    Args:
        UserRepositoryInterface (UserRepositoryInterface): Repository de l'utilisateur
    """

    def __init__(
        self, unit_of_work: SQLUnitOfWork, password_hasher: PasswordHasherInterface
    ):
        """Initialise le repository SQL pour les utilisateurs

        Args:
            unit_of_work (SQLUnitOfWork): Unité de travail SQL
            password_hasher (PasswordHasherInterface): Service de hachage de mot de passe
        """
        self.unit_of_work = unit_of_work
        self.password_hasher = password_hasher

    # write
    def sign_up_user(self, schema: UserEntity) -> UserEntity:
        """Enregistre un nouvel utilisateur

        Args:
            schema (UserEntity): Utilisateur à enregistrer

        Raises:
            UserDBException: L'utilisateur avec l'email spécifié existe déjà

        Returns:
            UserEntity: Utilisateur enregistré
        """
        with self.unit_of_work as uow:
            # Vérifier si l'utilisateur existe déjà
            query = select(UserSQLModel).where(UserSQLModel.email == schema.email)
            user = uow.session.exec(query).first()

            if user:
                raise UserDBException(
                    message=f"L'utilisateur avec l'email '{schema.email}' existe déjà."
                )

            # Hacher le mot de passe
            hashed_password = self.password_hasher.hash(schema.password)

            # Créer le modèle utilisateur
            user_model = UserSQLModel(
                id=schema.id,
                email=schema.email,
                password=hashed_password,
                role=schema.role,
                created_at=schema.created_at,
                updated_at=schema.updated_at,
            )

            # Enregistrer l'utilisateur
            uow.session.add(user_model)
            uow.session.flush()
            return user_model.to_entity()

    def delete_user_by_id(self, user_id: UUID) -> None:
        """Supprime un utilisateur par son identifiant

        Args:
            user_id (UUID): Identifiant de l'utilisateur à supprimer

        Raises:
            UserDBException: Exception de base de données
        """
        with self.unit_of_work as uow:
            user_to_delete = uow.session.get(UserSQLModel, user_id)
            if not user_to_delete:
                raise UserDBException(
                    message=f"L'utilisateur avec l'id '{user_id}' n'existe pas."
                )
            uow.session.delete(user_to_delete)
            uow.session.flush()

    # read
    def login_user(self, schema: UserEntity) -> UserEntity:
        """Connecte un utilisateur

        Args:
            schema (UserEntity): Utilisateur à connecter avec email et mot de passe

        Raises:
            UserDBException: L'utilisateur avec l'email spécifié n'existe pas
            UserDBException: Le mot de passe fourni est incorrect

        Returns:
        UserEntity: Utilisateur connecté
        """
        with self.unit_of_work as uow:
            query = select(UserSQLModel).where(UserSQLModel.email == schema.email)
            user = uow.session.exec(query).first()

            if not user:
                raise UserDBException(
                    message=f"L'utilisateur avec l'email '{schema.email}' n'existe pas."
                )

            if not self.password_hasher.verify(schema.password, user.password):
                raise UserDBException(message="Mot de passe incorrect.")

            return user.to_entity()

    def get_user_profile(self, user_id: UUID) -> UserEntity:
        """Récupère le profil d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur à récupérer

        Raises:
            UserDBException: Exception de base de données

        Returns:
            UserEntity: Utilisateur récupéré
        """
        with self.unit_of_work as uow:
            user = uow.session.get(UserSQLModel, user_id)
            if not user:
                raise UserDBException(
                    message=f"L'utilisateur avec l'id '{user_id}' n'existe pas."
                )

            return user.to_entity()

    def get_all_users_with_limit(self, limit: int) -> list[UserEntity]:
        """Récupère tous les utilisateurs avec une limite

        Args:
            limit (int): Limite de récupération

        Returns:
            list[UserEntity]: Liste des utilisateurs récupérés
        """
        with self.unit_of_work as uow:
            query = select(UserSQLModel).order_by(asc(UserSQLModel.email)).limit(limit)
            users = uow.session.exec(query).all()
            return [user.to_entity() for user in users]
