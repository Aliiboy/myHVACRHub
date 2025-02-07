from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.humid_air.get_full_ha_props import (
    GetFullHAPropertyUseCase,
)
from infra.web.container import AppContainer
from infra.web.dtos.generic import ClientErrorResponse
from infra.web.dtos.humid_air_dtos import HumidAirRequest, HumidAirResponse

tag = Tag(
    name="Air humide",
    description="Propriétés thermodynamiques de l'air humide - Hermann et al. ASHRAE ASHREA-RP1485",
)

router = APIBlueprint(
    "/humid_air",
    __name__,
    url_prefix="/humid_air",
    abp_tags=[tag],
    doc_ui=True,
)


@router.get(
    "/get_ha_props",
    description="Affiche l'ensemble des données disponibles pour l'air humide.",
    responses={
        HTTPStatus.OK: HumidAirResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ClientErrorResponse,
    },
)
@inject
def get_ha_props(
    query: HumidAirRequest,
    use_case: GetFullHAPropertyUseCase = Provide[
        AppContainer.get_full_ha_props_usecase
    ],
) -> Response:
    try:
        full_ha_props = use_case.execute(
            pressure=query.pressure,
            temp_dry_bulb=query.temp_dry_bulb,
            relative_humidity=query.relative_humidity,
        )
        return HumidAirResponse.from_use_case_result(full_ha_props).to_response()

    except ValueError as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()
