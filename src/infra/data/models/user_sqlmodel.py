from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from domain.entities.user.user_entity import User, UserRole
from domain.settings.user_settings import UserSettings


class UserSQLModel(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(primary_key=True, description=UserSettings.id_description)
    email: EmailStr = Field(
        unique=True, index=True, description=UserSettings.email_description
    )
    password: str = Field(description=UserSettings.password_description)
    role: UserRole = Field(description=UserSettings.role_description)
    created_at: datetime = Field(description=UserSettings.created_at_description)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            password=self.password,
            role=self.role,
            created_at=self.created_at,
        )
