from pydantic import BaseModel, Field
from pyfluids import HumidAir, InputHumidAir  #  type: ignore[import-untyped]

from humid_air.domain.settings.humid_air_settings import (
    HumidAirSettings,
)


class HumidAirEntity(BaseModel):
    pressure: float = Field(
        default=HumidAirSettings.pressure_default_value,
        ge=HumidAirSettings.pressure_ge,
        le=HumidAirSettings.pressure_le,
    )
    temp_dry_bulb: float = Field(
        ...,
        ge=HumidAirSettings.tdb_ge,
        le=HumidAirSettings.tdb_le,
    )
    relative_humidity: float = Field(
        ...,
        ge=HumidAirSettings.rh_ge,
        le=HumidAirSettings.rh_le,
    )

    def _get_humid_air_instance(self) -> HumidAir:
        return HumidAir().with_state(
            InputHumidAir.pressure(self.pressure),
            InputHumidAir.temperature(self.temp_dry_bulb),
            InputHumidAir.relative_humidity(self.relative_humidity),
        )

    @property
    def partial_pressure_of_water_vapor(self) -> HumidAir:
        return round(self._get_humid_air_instance().partial_pressure, 2)

    @property
    def humidity_ratio(self) -> HumidAir:
        return round(self._get_humid_air_instance().humidity, 6)

    @property
    def temp_dew_point(self) -> HumidAir:
        return round(self._get_humid_air_instance().dew_temperature, 2)

    @property
    def temp_wet_bulb(self) -> HumidAir:
        return round(self._get_humid_air_instance().wet_bulb_temperature, 2)

    @property
    def enthalpy_per_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().enthalpy, 0)

    @property
    def specific_heat_per_unit_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().specific_heat, 2)

    @property
    def entropy_per_unit_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().entropy, 2)

    @property
    def specific_volume_per_unit_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().specific_volume, 3)

    @property
    def density_per_unit_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().density, 3)

    @property
    def thermal_conductivity(self) -> HumidAir:
        return round(self._get_humid_air_instance().conductivity, 4)

    @property
    def dynamic_viscosity(self) -> HumidAir:
        return round(self._get_humid_air_instance().dynamic_viscosity, 8)

    @property
    def kinematic_viscosity_per_unit_humid_air(self) -> HumidAir:
        return round(self._get_humid_air_instance().kinematic_viscosity, 8)

    @property
    def prandtl_number(self) -> HumidAir:
        return round(self._get_humid_air_instance().prandtl, 2)

    @property
    def compressibility_factor(self) -> HumidAir:
        return round(self._get_humid_air_instance().compressibility, 4)
