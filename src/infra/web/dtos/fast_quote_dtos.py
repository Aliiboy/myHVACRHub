from enum import Enum
from http import HTTPStatus

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field, PositiveFloat

from domain.entities.fast_quote.cold_room_entity import ColdRoom, ColdRoomCategory
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
    type: ColdRoomCategory = Field(
        description=ColdRoomSettings.type_description,
        default=ColdRoomCategory.CF,
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
    type: ColdRoomCategory = Field(...)

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
            type=cold_room.category,
            volume=cold_room.volume,
            cooling_load=cooling_load,
        )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), HTTPStatus.OK)


class AddCoolingLoadFastCoefficientRequest(BaseModel):
    category: ColdRoomCategory = Field(..., description="Type de chambre froide")
    vol_min: int = Field(..., description="Volume minimum en m³")
    vol_max: int = Field(..., description="Volume maximum en m³")
    coef: int = Field(..., description="Coefficient ratio")


# =========== DTO ===========


class LocalFrigoRequest(BaseModel):
    puissance_frigo_local: float = Field(
        default=0, description="Puissance frigorifique en kW"
    )
    nb_appareils: float = Field(default=0, description="Nombre d'appareil")
    type_diffusion: str = Field(
        ..., description="Type de diffusion (SF ou DF exclusivement)"
    )
    type_degivrage: str = Field(
        ..., description="Type de dégivrage (DA ou DE exclusivement)"
    )


class GroupeFroidEnum(str, Enum):
    CHILLER_TRANE_1234ZE = "CHILLER_TRANE_1234ZE"
    CHILLER_CTA_R290 = "CHILLER_CTA_R290"
    CHILLER_INTERCON_NH3 = "CHILLER_INTERCON_NH3"


class GroupeFroidRequest(BaseModel):
    puissance_bilan_thermique: float = Field(
        ..., ge=200, description="Puissance bilan thermique en kW"
    )
    modele_GF: GroupeFroidEnum = Field(description="Modele de groupe froid")


class TuyauterieRequest(BaseModel):
    longueur_aller: float = Field(..., description="Longueur aller de tuyauterie")
    difficulte: float = Field(
        default=0, description="Poucentage de difficulté (25% doit etre 0,25)"
    )
    p_min: float = Field(default=0, description="Puissance minimale (en kW)")
    p_max: float = Field(default=0, description="Puissance maximale en kW")


class PrixTotal(BaseModel):
    prix_total: float = Field(default=0, description="Prix total")
