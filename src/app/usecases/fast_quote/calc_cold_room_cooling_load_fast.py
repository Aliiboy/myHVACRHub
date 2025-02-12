from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cold_room_entity import ColdRoom, ColdRoomCategory


class CalculateColdRoomCoolingLoadFastUseCase:
    def __init__(
        self,
        repository: ColdRoomCoolingCoefficientRepositoryInterface,
    ):
        self.repository = repository

    # TODO : change request
    # TODO : Pas forcé de renvoyer l'entité, le resultat de cooling_load suffirait.
    def execute(
        self, length: float, wigth: float, height: float, type: ColdRoomCategory
    ) -> tuple[ColdRoom, float]:
        cold_room = ColdRoom(
            length=length,
            width=wigth,
            height=height,
            category=type,
        )
        coef_by_category_and_volume = self.repository.get_coef_by_category_and_volume(
            cold_room
        )

        if coef_by_category_and_volume is None:
            raise ValueError("Aucun coefficient trouvé")

        cooling_load: float = round(
            ((cold_room.volume * coef_by_category_and_volume) / 1000), 2
        )
        return cold_room, cooling_load
