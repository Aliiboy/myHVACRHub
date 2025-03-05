from pydantic import BaseModel


class UserSignUpSchema(BaseModel):
    """Schéma pour l'inscription d'un utilisateur"""

    email: str
    password: str


class UserLoginSchema(BaseModel):
    """Schéma pour le login d'un utilisateur"""

    email: str
    password: str
