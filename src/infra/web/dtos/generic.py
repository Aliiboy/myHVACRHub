from http import HTTPStatus

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """200"""

    code: int = Field(default=HTTPStatus.OK, description="Status Code")
    message: str = Field(default="OK", description="Success message")

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), self.code)


class ClientErrorResponse(BaseModel):
    """400"""

    code: int = Field(default=HTTPStatus.BAD_REQUEST, description="Status Code")
    message: str | list[dict] = Field(
        default="Bad Request", description="Client error message"
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), self.code)
