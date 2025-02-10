from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from domain.entities.fast_quote.cold_room_entity import ColdRoomCategory


class CoolingLoadFastCoefficient(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="ID du coefficient")
    category: ColdRoomCategory = Field(..., description="Type de chambre froide")
    vol_min: int = Field(..., description="Volume mini en m³")
    vol_max: int = Field(..., description="Volume maxi en m³")
    coef: int = Field(..., description="Coefficient de charge frigorifique en W/m³")
