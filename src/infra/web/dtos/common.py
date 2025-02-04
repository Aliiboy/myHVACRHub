from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: int = Field(..., description="Status Code")
    message: str = Field(..., description="Error message")
