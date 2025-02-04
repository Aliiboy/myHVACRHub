from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify, make_response
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from infra.web.container import AppContainer
from infra.web.dtos.common import ErrorResponse
from infra.web.dtos.ha_dtos import HumidAirRequestDTO, HumidAirResponseDTO

tag = Tag(
    name="Air humide",
    description="Propriétés thermodynamiques de l'air humide - Hermann et al. ASHRAE ASHREA-RP1485",
)

router = APIBlueprint(
    "/humid_air",
    __name__,
    url_prefix="/humid_air",
    abp_tags=[tag],
    abp_responses={"400": ErrorResponse, "422": ErrorResponse, "500": ErrorResponse},
    doc_ui=True,
)


@router.get(
    "/get_ha_props",
    description="Affiche l'ensemble des données disponibles pour l'air humide.",
    responses={200: HumidAirResponseDTO},
)
@inject
def get_ha_props(
    query: HumidAirRequestDTO,
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

        response_data = {
            field: getattr(full_ha_props, field)
            for field in HumidAirResponseDTO.model_fields.keys()
        }
        response = HumidAirResponseDTO(**response_data)

        return make_response(jsonify(response.model_dump()), 200)

    except ValueError as e:
        return make_response(
            jsonify(
                ErrorResponse(code=422, message=f"Invalid input: {str(e)}").model_dump()
            ),
            422,
        )
