from abc import ABC, abstractmethod

from domain.entities.fast_quote.cold_room_entity import ColdRoom


class FastQuoteRepositoryInterface(ABC):
    @abstractmethod
    def get_cooling_load_fast_coefficient(self, cold_room: ColdRoom) -> int:
        pass
