from collections.abc import Callable
from http import HTTPStatus
from typing import cast

from flask import Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from infra.web.decorators.role_required import (
    role_required,
)
from infra.web.dtos.generic import SuccessResponse

tag = Tag(name="Routes proteges", description="Test des routes proteges")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/protected",
    __name__,
    url_prefix="/protected",
    abp_tags=[tag],
    abp_security=security,
    doc_ui=True,
)


@router.get("/")
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("moderator"))
def protected_route() -> Response:
    current_user = get_jwt_identity()
    return SuccessResponse(
        code=HTTPStatus.OK, message=f"Bienvenue,{current_user}"
    ).to_response()
