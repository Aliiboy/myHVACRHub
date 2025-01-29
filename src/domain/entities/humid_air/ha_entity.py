from CoolProp.HumidAirProp import HAPropsSI  # type: ignore[import-untyped]
from pydantic import BaseModel, Field, PositiveFloat

from domain.settings.ha_settings import HumidAirSettings


class HumidAir(BaseModel):
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

    def _get_ha_property(self, prop: str) -> PositiveFloat:
        return float(
            HAPropsSI(
                prop,
                "P",
                self.pressure,
                "T",
                self.temp_dry_bulb + 273.15,
                "RelHum",
                self.relative_humidity,
            )
        )

    @property
    def humidity_ratio(self) -> PositiveFloat:
        return round(self._get_ha_property("HumRat"), 6)

    @property
    def temp_dew_point(self) -> PositiveFloat:
        return round(self._get_ha_property("DewPoint") - 273.15, 2)

    @property
    def temp_wet_bulb(self) -> PositiveFloat:
        return round(self._get_ha_property("WetBulb") - 273.15, 2)

    @property
    def enthalpy_per_dry_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Enthalpy"), 0)

    @property
    def enthalpy_per_humid_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Hha"), 0)

    @property
    def specific_heat_per_unit_dry_air(self) -> PositiveFloat:
        return round(self._get_ha_property("C"), 2)

    @property
    def specific_heat_per_unit_humid_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Cha"), 2)

    @property
    def specific_heat_at_constant_volume_per_unit_dry_air(self) -> PositiveFloat:
        return round(self._get_ha_property("CV"), 2)

    @property
    def specific_heat_at_constant_volume_per_unit_humid_air(self) -> PositiveFloat:
        return round(self._get_ha_property("CVha"), 2)

    @property
    def entropy_per_unit_dry_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Entropy"), 2)

    @property
    def entropy_per_unit_humid_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Sha"), 2)

    @property
    def volume_per_unit_dry_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Vda"), 3)

    @property
    def volume_per_unit_humid_air(self) -> PositiveFloat:
        return round(self._get_ha_property("Vha"), 3)

    @property
    def density_per_unit_dry_air(self) -> PositiveFloat:
        return round(1 / self._get_ha_property("Vda"), 3)

    @property
    def density_per_unit_humid_air(self) -> PositiveFloat:
        return round(1 / self._get_ha_property("Vha"), 3)

    @property
    def thermal_conductivity(self) -> PositiveFloat:
        return round(self._get_ha_property("Conductivity"), 4)

    @property
    def dynamic_viscosity(self) -> PositiveFloat:
        return round(self._get_ha_property("Visc"), 8)

    @property
    def kinematic_viscosity_per_unit_dry_air(self) -> PositiveFloat:
        density_per_unit_dry_air = 1 / self._get_ha_property("Vda")
        dynamic_viscosity = self._get_ha_property("Visc")
        return round(dynamic_viscosity / density_per_unit_dry_air, 8)

    @property
    def kinematic_viscosity_per_unit_humid_air(self) -> PositiveFloat:
        density_per_unit_humid_air = 1 / self._get_ha_property("Vha")
        dynamic_viscosity = self._get_ha_property("Visc")
        return round(dynamic_viscosity / density_per_unit_humid_air, 8)

    @property
    def water_mole_fraction(self) -> PositiveFloat:
        return round(self._get_ha_property("psi_w"), 4)

    @property
    def compressibility_factor(self) -> PositiveFloat:
        return round(self._get_ha_property("Z"), 4)
