from collections.abc import Callable
from http import HTTPStatus
from typing import cast

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.fast_quote.get_cold_room_cooling_load_fast import (
    GetColdRoomCoolingLoadFastUseCase,
)
from infra.web.container import AppContainer
from infra.web.dtos.fast_quote_dtos import ColdRoomRequest, ColdRoomResponse
from infra.web.dtos.generic import ClientErrorResponse

tag = Tag(name="Chiffrage rapide", description="Genere un chiffrage rapide")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/fast_quote",
    __name__,
    url_prefix="/fast_quote",
    abp_tags=[tag],
    doc_ui=True,
)


@router.get(
    "get_cold_room_cooling_load_fast",
    description="Determine la puissance frigorifique d'une chambre froide (au ratio)",
    security=security,
    responses={
        HTTPStatus.OK: ColdRoomResponse,
        HTTPStatus.UNAUTHORIZED: ClientErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@inject
def get_cold_room_cooling_load_fast(
    query: ColdRoomRequest,
    use_case: GetColdRoomCoolingLoadFastUseCase = Provide[
        AppContainer.get_cold_room_cooling_load_fast_usecase
    ],
) -> Response:
    cold_room, cold_room_power = use_case.execute(
        query.length, query.width, query.height, query.type
    )

    return ColdRoomResponse.from_use_case_result(
        cold_room, cold_room_power
    ).to_response()
