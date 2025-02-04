from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):
    @abstractmethod
    def generate_token(self, user_id: str) -> str:
        pass
