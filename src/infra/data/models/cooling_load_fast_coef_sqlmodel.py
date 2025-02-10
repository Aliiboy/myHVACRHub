from uuid import UUID

from sqlmodel import Field, SQLModel

from domain.entities.fast_quote.cold_room_entity import ColdRoomCategory
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)


class CoolingLoadFastCoefficientSQLModel(SQLModel, table=True):
    __tablename__ = "cooling_load_fast_coefficient"

    id: UUID = Field(primary_key=True, index=True)
    category: ColdRoomCategory = Field(index=True)
    vol_min: int = Field(
        ...,
    )
    vol_max: int = Field(
        ...,
    )
    coef: int = Field(
        ...,
    )

    def to_entity(self) -> CoolingLoadFastCoefficient:
        return CoolingLoadFastCoefficient(
            id=self.id,
            category=self.category,
            vol_min=self.vol_min,
            vol_max=self.vol_max,
            coef=self.coef,
        )
