from http import HTTPStatus

from flask import Response, jsonify, make_response
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Réponse de succès

    Args:
        BaseModel (BaseModel): Modèle de base

    Returns:
        Response: Réponse de succès
    """

    code: int = Field(default=HTTPStatus.OK, description="Status Code")
    message: str = Field(default="OK", description="Success message")

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), self.code)


class ErrorResponse(BaseModel):
    """Réponse d'erreur

    Args:
        BaseModel (BaseModel): Modèle de base

    Returns:
        Response: Réponse d'erreur
    """

    code: int = Field(default=HTTPStatus.BAD_REQUEST, description="Status Code")
    message: str | list[dict[str, str]] = Field(
        default="Bad Request", description="Client error message"
    )

    def to_response(self) -> Response:
        return make_response(jsonify(self.model_dump()), self.code)
