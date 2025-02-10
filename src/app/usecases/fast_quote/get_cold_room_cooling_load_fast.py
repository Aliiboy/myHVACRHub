from app.repositories.fast_quote_interface import FastQuoteRepositoryInterface
from domain.entities.fast_quote.cold_room_entity import ColdRoom, ColdRoomType


class GetColdRoomCoolingLoadFastUseCase:
    def __init__(
        self,
        repository: FastQuoteRepositoryInterface,
    ):
        self.repository = repository

    def execute(
        self, length: float, wigth: float, height: float, type: ColdRoomType
    ) -> tuple[ColdRoom, float]:
        cold_room = ColdRoom(
            length=length,
            width=wigth,
            height=height,
            type=type,
        )
        cooling_load_fast_coefficient = (
            self.repository.get_cooling_load_fast_coefficient(cold_room)
        )

        cooling_load: float = round(
            ((cold_room.volume * cooling_load_fast_coefficient) / 1000), 2
        )

        return cold_room, cooling_load
