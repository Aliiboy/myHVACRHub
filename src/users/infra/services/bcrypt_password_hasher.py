import bcrypt

from users.domain.services.password_hasher_interface import PasswordHasherInterface


class BcryptPasswordHasher(PasswordHasherInterface):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())
