import unittest

from domain.exceptions.user_exceptions import UserInvalidPasswordPatternException
from infra.web.dtos.user_dtos import RegisterRequest


class UserDTOTests(unittest.TestCase):
    def test_valid_password(self) -> None:
        data = {"email": "test@example.com", "password": "Secure1!"}
        dto = RegisterRequest(**data)
        self.assertEqual(dto.email, "test@example.com")

    def test_invalid_password_no_special_character(self) -> None:
        data = {"email": "test@example.com", "password": "Secure1"}
        with self.assertRaises(UserInvalidPasswordPatternException):
            RegisterRequest(**data)

    def test_invalid_password_no_digit(self) -> None:
        data = {"email": "test@example.com", "password": "SecurePass!"}
        with self.assertRaises(UserInvalidPasswordPatternException):
            RegisterRequest(**data)
