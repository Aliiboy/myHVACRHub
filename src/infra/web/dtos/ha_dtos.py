from pydantic import BaseModel, Field

from domain.settings.ha_settings import HumidAirSettings


class HumidAirRequestDTO(BaseModel):
    pressure: float = Field(
        default=HumidAirSettings.pressure_default_value,
        description=HumidAirSettings.pressure_description,
        ge=HumidAirSettings.pressure_ge,
        le=HumidAirSettings.pressure_le,
    )
    temp_dry_bulb: float = Field(
        ...,
        description=HumidAirSettings.tdb_description,
        ge=HumidAirSettings.tdb_ge,
        le=HumidAirSettings.tdb_le,
    )
    relative_humidity: float = Field(
        ...,
        description=HumidAirSettings.rh_description,
        ge=HumidAirSettings.rh_ge,
        le=HumidAirSettings.rh_le,
    )


class HumidAirResponseDTO(BaseModel):
    pressure: float = Field(..., description=HumidAirSettings.pressure_description)
    temp_dry_bulb: float = Field(..., description=HumidAirSettings.tdb_description)
    relative_humidity: float = Field(..., description=HumidAirSettings.rh_description)
    partial_pressure_of_water_vapor: float = Field(
        ..., description=HumidAirSettings.partial_pressure_of_water_vapor
    )
    humidity_ratio: float = Field(
        ..., description=HumidAirSettings.humidity_ratio_description
    )
    temp_dew_point: float = Field(
        ..., description=HumidAirSettings.temp_dew_point_description
    )
    temp_wet_bulb: float = Field(
        ..., description=HumidAirSettings.temp_wet_bulb_description
    )
    enthalpy_per_humid_air: float = Field(
        ..., description=HumidAirSettings.enthalpy_per_humid_air_description
    )
    specific_heat_per_unit_humid_air: float = Field(
        ..., description=HumidAirSettings.specific_heat_per_unit_humid_air_description
    )
    entropy_per_unit_humid_air: float = Field(
        ..., description=HumidAirSettings.entropy_per_unit_humid_air_description
    )
    specific_volume_per_unit_humid_air: float = Field(
        ..., description=HumidAirSettings.specific_volume_per_unit_humid_air_description
    )
    density_per_unit_humid_air: float = Field(
        ..., description=HumidAirSettings.density_per_unit_humid_air_description
    )
    thermal_conductivity: float = Field(
        ..., description=HumidAirSettings.thermal_conductivity_description
    )
    dynamic_viscosity: float = Field(
        ..., description=HumidAirSettings.dynamic_viscosity_description
    )
    kinematic_viscosity_per_unit_humid_air: float = Field(
        ...,
        description=HumidAirSettings.kinematic_viscosity_per_unit_humid_air_description,
    )
    prandtl_number: float = Field(
        ..., description=HumidAirSettings.prandtl_number_description
    )
    compressibility_factor: float = Field(
        ..., description=HumidAirSettings.compressibility_factor_description
    )
