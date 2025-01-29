from typing import Any

from dependency_injector.wiring import Provide, inject
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from infra.web.container import AppContainer
from infra.web.dtos.ha_dtos import HumidAirRequestDTO, HumidAirResponseDTO

tag = Tag(
    name="Air humide",
    description="Propriétés thermodynamique de l'air humide - Hermann et al. ASHRAE ASHREA-RP1485",
)
router = APIBlueprint(
    "/humid_air",
    __name__,
    url_prefix="/humid_air",
    abp_tags=[tag],
    doc_ui=True,
)


@router.get(
    "/get_full_ha_props",
    description="Affiche l'ensemble des données disponible.",
    responses={200: HumidAirResponseDTO},
)
@inject
def get_full_ha_props(
    query: HumidAirRequestDTO,
    use_case: GetFullHAPropertyUseCase = Provide[
        AppContainer.get_full_ha_props_usecase
    ],
) -> dict[str, Any]:
    full_ha_props = use_case.execute(
        temp_dry_bulb=query.temp_dry_bulb,
        relative_humidity=query.relative_humidity,
    )
    response = HumidAirResponseDTO(
        pressure=full_ha_props.pressure,
        temp_dry_bulb=full_ha_props.temp_dry_bulb,
        relative_humidity=full_ha_props.relative_humidity,
        humidity_ratio=full_ha_props.humidity_ratio,
        temp_dew_point=full_ha_props.temp_dew_point,
        temp_wet_bulb=full_ha_props.temp_wet_bulb,
        enthalpy_per_dry_air=full_ha_props.enthalpy_per_dry_air,
        enthalpy_per_humid_air=full_ha_props.enthalpy_per_humid_air,
        specific_heat_per_unit_dry_air=full_ha_props.specific_heat_per_unit_dry_air,
        specific_heat_per_unit_humid_air=full_ha_props.specific_heat_per_unit_humid_air,
        specific_heat_at_constant_volume_per_unit_dry_air=full_ha_props.specific_heat_at_constant_volume_per_unit_dry_air,
        specific_heat_at_constant_volume_per_unit_humid_air=full_ha_props.specific_heat_at_constant_volume_per_unit_humid_air,
        entropy_per_unit_dry_air=full_ha_props.entropy_per_unit_dry_air,
        entropy_per_unit_humid_air=full_ha_props.entropy_per_unit_humid_air,
        volume_per_unit_dry_air=full_ha_props.volume_per_unit_dry_air,
        volume_per_unit_humid_air=full_ha_props.volume_per_unit_humid_air,
        density_per_unit_dry_air=full_ha_props.density_per_unit_dry_air,
        density_per_unit_humid_air=full_ha_props.density_per_unit_humid_air,
        thermal_conductivity=full_ha_props.thermal_conductivity,
        dynamic_viscosity=full_ha_props.dynamic_viscosity,
        kinematic_viscosity_per_unit_dry_air=full_ha_props.kinematic_viscosity_per_unit_dry_air,
        kinematic_viscosity_per_unit_humid_air=full_ha_props.kinematic_viscosity_per_unit_humid_air,
        water_mole_fraction=full_ha_props.water_mole_fraction,
        compressibility_factor=full_ha_props.compressibility_factor,
    )

    return response.model_dump()
