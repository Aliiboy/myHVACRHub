from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)


class GetAllCoolingLoadFastCoefficienUseCase:
    def __init__(self, repository: ColdRoomCoolingCoefficientRepositoryInterface):
        self.repository = repository

    # TODO : change request
    def execute(self, limit: int) -> list[CoolingLoadFastCoefficient]:
        return self.repository.get_all_coefficients(limit)
