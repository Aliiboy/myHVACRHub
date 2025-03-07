from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from common.infra.web.container import AppContainer
from common.infra.web.dtos.generic import ErrorResponse
from humid_air.app.schemas.get_ha_props_schema import GetHumidAirPropertySchema
from humid_air.app.usecases.get_ha_props import GetHumidAirPropertyUseCase
from humid_air.infra.web.dtos.humid_air_dtos import (
    GetHumidAirPropertyResponse,
    HumidAirWithDryTemperatureAndRelativeHumidityRequest,
)

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
        HTTPStatus.OK: GetHumidAirPropertyResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorResponse,
    },
)
@inject
def get_ha_props(
    query: HumidAirWithDryTemperatureAndRelativeHumidityRequest,
    use_case: GetHumidAirPropertyUseCase = Provide[
        AppContainer.humid_air_usecases.provided["get_ha_props"]
    ],
) -> Response:
    try:
        request = GetHumidAirPropertySchema(
            pressure=query.pressure,
            temp_dry_bulb=query.temp_dry_bulb,
            relative_humidity=query.relative_humidity,
        )
        full_ha_props = use_case.execute(request)
        return GetHumidAirPropertyResponse.from_use_case_result(
            full_ha_props
        ).to_response()

    except ValueError as e:
        return ErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()
