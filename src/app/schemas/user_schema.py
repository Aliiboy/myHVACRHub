from pydantic import BaseModel


class UserSignUpSchema(BaseModel):
    email: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str
