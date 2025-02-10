from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cold_room_entity import ColdRoomCategory
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)


class AddCoolingLoadFastCoefficientUseCase:
    def __init__(self, repository: ColdRoomCoolingCoefficientRepositoryInterface):
        self.repository = repository

    def execute(
        self, category: ColdRoomCategory, vol_min: int, vol_max: int, coef: int
    ) -> CoolingLoadFastCoefficient:
        coefficient = CoolingLoadFastCoefficient(
            category=category,
            vol_min=vol_min,
            vol_max=vol_max,
            coef=coef,
        )
        self.repository.add_coefficient(coefficient)
        return coefficient
