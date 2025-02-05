from collections.abc import Callable
from typing import cast

from flask import Response, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from infra.web.decorators.role_required_decorator import role_required
from infra.web.dtos.common import ErrorResponse

tag = Tag(name="Routes proteges", description="Test des routes proteges")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/protected",
    __name__,
    url_prefix="/protected",
    abp_tags=[tag],
    abp_responses={"401": ErrorResponse, "422": ErrorResponse, "500": ErrorResponse},
    abp_security=security,
    doc_ui=True,
)


@router.get("/protected")
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("moderator"))
def protected_route() -> Response:
    current_user = get_jwt_identity()
    return make_response(jsonify({"message": f"Bienvenue, {current_user}"}), 200)
