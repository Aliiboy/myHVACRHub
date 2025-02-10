from http import HTTPStatus

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field, PositiveFloat

from domain.entities.fast_quote.cold_room_entity import ColdRoom, ColdRoomType
from domain.settings.cold_room_settings import ColdRoomSettings


class ColdRoomRequest(BaseModel):
    length: float = Field(
        ...,
        description=ColdRoomSettings.length_description,
        ge=ColdRoomSettings.length_ge,
        le=ColdRoomSettings.length_le,
    )
    width: float = Field(
        ...,
        description=ColdRoomSettings.width_description,
        ge=ColdRoomSettings.width_ge,
        le=ColdRoomSettings.width_le,
    )
    height: float = Field(
        ...,
        description=ColdRoomSettings.height_description,
        ge=ColdRoomSettings.height_ge,
        le=ColdRoomSettings.height_le,
    )
    type: ColdRoomType = Field(
        description=ColdRoomSettings.type_description,
        default=ColdRoomType.CF,
    )


class ColdRoomResponse(BaseModel):
    length: PositiveFloat = Field(
        ...,
        description=ColdRoomSettings.length_description,
    )
    width: PositiveFloat = Field(
        ...,
        description=ColdRoomSettings.width_description,
        ge=ColdRoomSettings.width_ge,
        le=ColdRoomSettings.width_le,
    )
    height: PositiveFloat = Field(
        ...,
        description=ColdRoomSettings.height_description,
    )
    type: ColdRoomType = Field(...)

    volume: PositiveFloat = Field(..., description=ColdRoomSettings.volume_description)

    cooling_load: PositiveFloat = Field(
        ..., description="Puissance frigorifique en [kW]"
    )

    @classmethod
    def from_use_case_result(
        cls, cold_room: ColdRoom, cooling_load: float
    ) -> "ColdRoomResponse":
        return cls(
            length=cold_room.length,
            width=cold_room.width,
            height=cold_room.height,
            type=cold_room.type,
            volume=cold_room.volume,
            cooling_load=cooling_load,
        )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)
