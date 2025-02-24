from abc import ABC, abstractmethod
from uuid import UUID

from users.domain.entities.user_entity import UserRole


class TokenServiceInterface(ABC):
    @abstractmethod
    def generate_token(self, user_id: UUID, role: UserRole) -> str:
        pass
