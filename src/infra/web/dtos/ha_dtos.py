from pydantic import BaseModel, Field, PositiveFloat

from domain.settings.ha_settings import HumidAirSettings


class HumidAirRequestDTO(BaseModel):
    pressure: PositiveFloat = Field(
        default=HumidAirSettings.pressure_default_value,
        description=HumidAirSettings.pressure_description,
    )
    temp_dry_bulb: PositiveFloat = Field(
        ...,
        description=HumidAirSettings.tdb_description,
        ge=HumidAirSettings.tdb_ge,
        le=HumidAirSettings.tdb_le,
    )
    relative_humidity: PositiveFloat = Field(
        ...,
        description=HumidAirSettings.rh_description,
        ge=HumidAirSettings.rh_ge,
        le=HumidAirSettings.rh_le,
    )


class HumidAirResponseDTO(BaseModel):
    pressure: PositiveFloat = Field(description=HumidAirSettings.pressure_description)
    temp_dry_bulb: PositiveFloat = Field(description=HumidAirSettings.tdb_description)
    relative_humidity: PositiveFloat = Field(
        description=HumidAirSettings.rh_description
    )
    humidity_ratio: PositiveFloat = Field(
        description=HumidAirSettings.humidity_ratio_description
    )
    temp_dew_point: PositiveFloat = Field(
        description=HumidAirSettings.temp_dew_point_description
    )
    temp_wet_bulb: PositiveFloat = Field(
        description=HumidAirSettings.temp_wet_bulb_description
    )
    enthalpy_per_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.enthalpy_per_dry_air_description
    )
    enthalpy_per_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.enthalpy_per_humid_air_description
    )
    specific_heat_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.specific_heat_per_unit_dry_air_description
    )
    specific_heat_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.specific_heat_per_unit_humid_air_description
    )
    specific_heat_at_constant_volume_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.specific_heat_at_constant_volume_per_unit_dry_air_description
    )
    specific_heat_at_constant_volume_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.specific_heat_at_constant_volume_per_unit_humid_air_description
    )
    entropy_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.entropy_per_unit_dry_air_description
    )
    entropy_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.entropy_per_unit_humid_air_description
    )
    volume_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.volume_per_unit_dry_air_description
    )
    volume_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.volume_per_unit_humid_air_description
    )
    density_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.density_per_unit_dry_air_description
    )
    density_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.density_per_unit_humid_air_description
    )
    thermal_conductivity: PositiveFloat = Field(
        description=HumidAirSettings.thermal_conductivity_description
    )
    dynamic_viscosity: PositiveFloat = Field(
        description=HumidAirSettings.dynamic_viscosity_description
    )
    kinematic_viscosity_per_unit_dry_air: PositiveFloat = Field(
        description=HumidAirSettings.kinematic_viscosity_per_unit_dry_air_description
    )
    kinematic_viscosity_per_unit_humid_air: PositiveFloat = Field(
        description=HumidAirSettings.kinematic_viscosity_per_unit_humid_air_description
    )
    water_mole_fraction: PositiveFloat = Field(
        description=HumidAirSettings.water_mole_fraction_description
    )
    compressibility_factor: PositiveFloat = Field(
        description=HumidAirSettings.compressibility_factor_description
    )
