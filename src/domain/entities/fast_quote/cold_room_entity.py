from enum import Enum

from pydantic import BaseModel, Field, PositiveFloat

from domain.settings.cold_room_settings import ColdRoomSettings


class ColdRoomType(str, Enum):
    QUAI = "QUAI"
    CF = "CF"
    PLATEFORME = "PLATEFORME"


class ColdRoom(BaseModel):
    length: PositiveFloat = Field(
        ...,
        ge=ColdRoomSettings.length_ge,
        le=ColdRoomSettings.length_le,
    )
    width: PositiveFloat = Field(
        ...,
        ge=ColdRoomSettings.width_ge,
        le=ColdRoomSettings.width_le,
    )
    height: PositiveFloat = Field(
        ...,
        ge=ColdRoomSettings.height_ge,
        le=ColdRoomSettings.height_le,
    )
    type: ColdRoomType = Field(
        default=ColdRoomType.CF,
    )

    @property
    def volume(self) -> PositiveFloat:
        return round((self.length * self.width * self.height), 2)
