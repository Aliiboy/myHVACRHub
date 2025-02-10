from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from domain.entities.user.user_entity import User, UserRole


class UserSQLModel(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str = Field()
    role: UserRole = Field()
    created_at: datetime = Field()

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            password=self.password,
            role=self.role,
            created_at=self.created_at,
        )
