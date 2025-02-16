from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from domain.settings.user_settings import UserSettings


class UserRole(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(
        ...,
    )
    password: str = Field(
        ...,
        min_length=UserSettings.password_min_length,
        pattern=UserSettings.password_pattern,
    )
    role: UserRole = Field(default=UserRole.user)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
