from uuid import UUID

from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)
from domain.exceptions.fast_quote_exceptions import (
    CoolingLoadFastCoefficientNotFoundException,
)
from infra.web.dtos.fast_quote_dtos import CoolingLoadFastCoefficientBody


class UpdateCoolingLoadFastCoefficientUseCase:
    def __init__(self, repository: ColdRoomCoolingCoefficientRepositoryInterface):
        self.repository = repository

    # TODO : change request
    def execute(
        self, id: UUID, data: CoolingLoadFastCoefficientBody
    ) -> CoolingLoadFastCoefficient:
        coefficient = self.repository.update_coefficient(id, data)
        if coefficient is None:
            raise CoolingLoadFastCoefficientNotFoundException(id)
        return coefficient
