from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from domain.settings.book_settings import BookEntitieSettings


class Book(BaseModel):
    id: UUID = Field(
        default_factory=uuid4, description=BookEntitieSettings.id_description
    )
    title: str = Field(
        ...,
        min_length=BookEntitieSettings.title_min_length,
        max_length=BookEntitieSettings.title_max_length,
        description=BookEntitieSettings.title_description,
    )
    author: str = Field(
        ...,
        min_length=BookEntitieSettings.author_min_length,
        max_length=BookEntitieSettings.author_max_length,
        description=BookEntitieSettings.author_description,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description=BookEntitieSettings.created_at_description,
    )

    @property
    def duration_in_days(self) -> int:
        return (datetime.utcnow() - self.created_at).days
