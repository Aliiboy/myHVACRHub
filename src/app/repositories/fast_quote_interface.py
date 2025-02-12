from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.fast_quote.cold_room_entity import ColdRoom
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)
from infra.web.dtos.fast_quote_dtos import CoolingLoadFastCoefficientBody


class ColdRoomCoolingCoefficientRepositoryInterface(ABC):
    # write
    @abstractmethod
    def add_coefficient(
        self, coefficient: CoolingLoadFastCoefficient
    ) -> CoolingLoadFastCoefficient:
        pass

    @abstractmethod
    def update_coefficient(
        self, id: UUID, data: CoolingLoadFastCoefficientBody
    ) -> CoolingLoadFastCoefficient | None:
        pass

    # read
    @abstractmethod
    def get_coef_by_category_and_volume(self, cold_room: ColdRoom) -> int | None:
        pass

    @abstractmethod
    def get_all_coefficients(self, limit: int) -> list[CoolingLoadFastCoefficient]:
        pass
