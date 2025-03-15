from uuid import UUID

from sqlmodel import and_, asc, select

from common.infra.data.sql_unit_of_work import SQLUnitOfWork
from projects.app.repositories.project_interface import ProjectRepositoryInterface
from projects.domain.entities.project_entity import (
    ProjectAndUserJonctionTableEntity,
    ProjectEntity,
    ProjectMemberRole,
)
from projects.domain.exceptions.project_exceptions import (
    ProjectDBException,
)
from projects.infra.data.models.project_sqlmodel import (
    ProjectAndUserJonctionTableSQLModel,
    ProjectSQLModel,
)
from users.domain.entities.user_entity import UserEntity
from users.infra.data.models.user_sqlmodel import UserSQLModel


class ProjectSQLRepository(ProjectRepositoryInterface):
    """Repository pour les projets

    Args:
        ProjectRepositoryInterface (ProjectRepositoryInterface): Repository de projet
    """

    def __init__(self, unit_of_work: SQLUnitOfWork):
        """Initialise le repository

        Args:
            unit_of_work (SQLUnitOfWork): Unit of work
        """
        self.unit_of_work = unit_of_work

    # write
    def create_project(self, schema: ProjectEntity, creator_id: UUID) -> ProjectEntity:
        """Crée un nouveau projet

        Args:
            schema (ProjectEntity): Projet à créer
            creator_id (UUID): Identifiant de l'utilisateur créateur

        Raises:
            ProjectDBException: Exception de base de données

        Returns:
            ProjectEntity: Projet créé
        """
        with self.unit_of_work as uow:
            # Vérifier si un projet avec le même nom existe déjà
            name_query = select(ProjectSQLModel).where(
                ProjectSQLModel.name == schema.name
            )
            existing_name = uow.session.exec(name_query).first()
            if existing_name:
                raise ProjectDBException(
                    message=f"Un projet avec le nom '{schema.name}' existe déjà."
                )

            # Vérifier si un projet avec le même numéro existe déjà
            number_query = select(ProjectSQLModel).where(
                ProjectSQLModel.project_number == schema.project_number
            )
            existing_number = uow.session.exec(number_query).first()
            if existing_number:
                raise ProjectDBException(
                    message=f"Un projet avec le numéro '{schema.project_number}' existe déjà."
                )

            # Vérifier si l'utilisateur créateur existe
            creator = uow.session.get(UserSQLModel, creator_id)
            if not creator:
                raise ProjectDBException(
                    message=f"L'utilisateur avec l'id '{creator_id}' n'existe pas."
                )

            # Créer le projet
            query = ProjectSQLModel(
                id=schema.id,
                project_number=schema.project_number,
                name=schema.name,
                description=schema.description,
                created_at=schema.created_at,
                updated_at=schema.updated_at,
            )
            uow.session.add(query)
            uow.session.flush()

            # Ajouter le créateur comme membre avec le rôle ADMIN
            member = ProjectAndUserJonctionTableSQLModel(
                project_id=schema.id,
                user_id=creator_id,
                role=ProjectMemberRole.ADMIN.value,
            )
            uow.session.add(member)
            uow.session.flush()

            return query.to_entity()

    def delete_project_by_id(self, project_id: UUID) -> None:
        """Supprime un projet par son identifiant

        Args:
            project_id (UUID): Identifiant du projet à supprimer

        Raises:
            ProjectDBException: Le projet n'existe pas
        """
        with self.unit_of_work as uow:
            project_to_delete = uow.session.get(ProjectSQLModel, project_id)
            if not project_to_delete:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{project_id}' n'existe pas."
                )
            uow.session.delete(project_to_delete)
            uow.session.flush()

    def update_project(self, schema: ProjectEntity) -> ProjectEntity:
        """Met à jour un projet

        Args:
            schema (ProjectEntity): Projet à mettre à jour

        Raises:
            ProjectDBException: Exception de base de données

        Returns:
            ProjectEntity: Projet mis à jour
        """
        with self.unit_of_work as uow:
            project_to_update = uow.session.get(ProjectSQLModel, schema.id)
            if not project_to_update:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{schema.id}' n'existe pas."
                )

            # Vérifier si le nom existe déjà pour un autre projet
            if project_to_update.name != schema.name:
                name_query = select(ProjectSQLModel).where(
                    ProjectSQLModel.name == schema.name,
                    ProjectSQLModel.id != schema.id,
                )
                existing_name = uow.session.exec(name_query).first()
                if existing_name:
                    raise ProjectDBException(
                        message=f"Un projet avec le nom '{schema.name}' existe déjà."
                    )

            # Vérifier si le numéro existe déjà pour un autre projet
            if project_to_update.project_number != schema.project_number:
                number_query = select(ProjectSQLModel).where(
                    ProjectSQLModel.project_number == schema.project_number,
                    ProjectSQLModel.id != schema.id,
                )
                existing_number = uow.session.exec(number_query).first()
                if existing_number:
                    raise ProjectDBException(
                        message=f"Un projet avec le numéro '{schema.project_number}' existe déjà."
                    )

            project_to_update.project_number = schema.project_number
            project_to_update.name = schema.name
            project_to_update.description = schema.description
            project_to_update.updated_at = schema.updated_at

            uow.session.add(project_to_update)
            uow.session.flush()
            return project_to_update.to_entity()

    def add_project_member(
        self,
        project_id: UUID,
        user_id: UUID,
        role: ProjectMemberRole,
    ) -> ProjectAndUserJonctionTableEntity:
        """Ajoute un membre à un projet

        Args:
            project_id (UUID): Identifiant du projet
            user_id (UUID): Identifiant de l'utilisateur à ajouter
            role (ProjectMemberRole): Rôle de l'utilisateur dans le projet

        Raises:
            ProjectDBException: Exception de base de données

        Returns:
            ProjectMemberLinkEntity: Membre du projet ajouté
        """
        with self.unit_of_work as uow:
            # Vérifier si le projet existe
            project = uow.session.get(ProjectSQLModel, project_id)
            if not project:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{project_id}' n'existe pas."
                )

            # Vérifier si l'utilisateur existe
            user = uow.session.get(UserSQLModel, user_id)
            if not user:
                raise ProjectDBException(
                    message=f"L'utilisateur avec l'id '{user_id}' n'existe pas."
                )

            # Vérifier si l'utilisateur est déjà membre du projet
            query = select(ProjectAndUserJonctionTableSQLModel).where(
                ProjectAndUserJonctionTableSQLModel.project_id == project_id,
                ProjectAndUserJonctionTableSQLModel.user_id == user_id,
            )
            existing_member = uow.session.exec(query).first()
            if existing_member:
                raise ProjectDBException(
                    message="L'utilisateur est déjà membre du projet."
                )

            # Ajouter le membre au projet
            member = ProjectAndUserJonctionTableSQLModel(
                project_id=project_id,
                user_id=user_id,
                role=role.value,
            )
            uow.session.add(member)
            uow.session.flush()
            return member.to_entity()

    def delete_project_member(self, project_id: UUID, user_id: UUID) -> None:
        """Supprime un membre d'un projet

        Args:
            project_id (UUID): Identifiant du projet
            user_id (UUID): Identifiant de l'utilisateur à supprimer

        Raises:
            ProjectDBException: Le projet n'existe pas
            ProjectDBException: Le membre n'existe pas
        """
        with self.unit_of_work as uow:
            # Vérifier si le projet existe
            project = uow.session.get(ProjectSQLModel, project_id)
            if not project:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{project_id}' n'existe pas."
                )

            # Vérifier si l'utilisateur est membre du projet
            query = select(ProjectAndUserJonctionTableSQLModel).where(
                ProjectAndUserJonctionTableSQLModel.project_id == project_id,
                ProjectAndUserJonctionTableSQLModel.user_id == user_id,
            )
            member = uow.session.exec(query).first()
            if not member:
                raise ProjectDBException(
                    message="L'utilisateur n'est pas membre du projet."
                )

            # Supprimer le membre du projet
            uow.session.delete(member)
            uow.session.flush()

    # read
    def get_project_by_id(self, project_id: UUID) -> ProjectEntity:
        """Récupère un projet par son identifiant

        Args:
            project_id (UUID): Identifiant du projet à récupérer

        Raises:
            ProjectDBException: Le projet n'existe pas

        Returns:
            ProjectEntity: Projet récupéré
        """
        with self.unit_of_work as uow:
            project = uow.session.get(ProjectSQLModel, project_id)
            if not project:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{project_id}' n'existe pas."
                )

            return project.to_entity()

    def get_all_projects_with_limit(self, limit: int) -> list[ProjectEntity]:
        """Récupère tous les projets avec une limite

        Args:
            limit (int): Limite de récupération

        Returns:
            list[ProjectEntity]: Liste des projets récupérés
        """
        with self.unit_of_work as uow:
            query = (
                select(ProjectSQLModel).order_by(asc(ProjectSQLModel.name)).limit(limit)
            )
            projects = uow.session.exec(query).all()
            return [project.to_entity() for project in projects]

    def get_user_projects(self, user_id: UUID) -> list[ProjectEntity]:
        """Récupère tous les projets d'un utilisateur

        Args:
            user_id (UUID): Identifiant de l'utilisateur

        Returns:
            list[ProjectEntity]: Liste des projets de l'utilisateur
        """
        with self.unit_of_work as uow:
            # Récupérer les projets dont l'utilisateur est membre
            query = (
                select(ProjectSQLModel)
                .join(
                    ProjectAndUserJonctionTableSQLModel,
                    and_(
                        ProjectSQLModel.id
                        == ProjectAndUserJonctionTableSQLModel.project_id
                    ),
                )
                .where(ProjectAndUserJonctionTableSQLModel.user_id == user_id)
            )
            projects = uow.session.exec(query).all()
            return [project.to_entity() for project in projects]

    def get_project_members(self, project_id: UUID) -> list[UserEntity]:
        """Récupère les membres d'un projet

        Args:
            project_id (UUID): Identifiant du projet

        Raises:
            ProjectDBException: Le projet n'existe pas

        Returns:
            list[UserEntity]: Liste des membres du projet
        """
        with self.unit_of_work as uow:
            # Vérifier si le projet existe
            project = uow.session.get(ProjectSQLModel, project_id)
            if not project:
                raise ProjectDBException(
                    message=f"Le projet avec l'id '{project_id}' n'existe pas."
                )

            # Récupérer les membres du projet
            query = (
                select(UserSQLModel)
                .join(ProjectAndUserJonctionTableSQLModel)
                .where(ProjectAndUserJonctionTableSQLModel.project_id == project_id)
            )
            members = uow.session.exec(query).all()
            return [member.to_entity(include_related=False) for member in members]
