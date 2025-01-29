from CoolProp.HumidAirProp import HAPropsSI  # type: ignore[import-untyped]
from pydantic import BaseModel, Field, PositiveFloat

from domain.settings.hair_settings import HumidAirSettings


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
        """Helper method to get a property from HAPropsSI."""
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
        """Humidity ratio in (kg water/kg dry air"""
        return round(self._get_ha_property("HumRat"), 6)

    @property
    def temp_dew_point(self) -> PositiveFloat:
        """Dew point temperature in °C"""
        return round(self._get_ha_property("DewPoint") - 273.15, 2)

    @property
    def temp_wet_bulb(self) -> PositiveFloat:
        """Wet bulb temperature in °C"""
        return round(self._get_ha_property("WetBulb") - 273.15, 2)

    @property
    def enthalpy_per_dry_air(self) -> PositiveFloat:
        """Enthalpy per kg of dry air (J/kg)"""
        return round(self._get_ha_property("Enthalpy"), 0)

    @property
    def enthalpy_per_humid_air(self) -> PositiveFloat:
        """Enthalpy per kg of humid air (J/kg)"""
        return round(self._get_ha_property("Hha"), 0)

    @property
    def specific_heat_per_unit_dry_air(self) -> PositiveFloat:
        """Specific heat capacity per unit (J/kg dry air.K)"""
        return round(self._get_ha_property("C"), 2)

    @property
    def specific_heat_per_unit_humid_air(self) -> PositiveFloat:
        """Specific heat capacity per unit (J/kg humid air.K)"""
        return round(self._get_ha_property("Cha"), 2)

    @property
    def specific_heat_at_constant_volume_per_unit_dry_air(self) -> PositiveFloat:
        """Specific heat capacity at constant volume (J/kg dry air.K)"""
        return round(self._get_ha_property("CV"), 2)

    @property
    def specific_heat_at_constant_volume_per_unit_humid_air(self) -> PositiveFloat:
        """Specific heat capacity at constant volume (J/kg humid air.K)"""
        return round(self._get_ha_property("CVha"), 2)

    @property
    def entropy_per_unit_dry_air(self) -> PositiveFloat:
        """Entropy per unit dry air (J/kg dry air.K)"""
        return round(self._get_ha_property("Entropy"), 2)

    @property
    def entropy_per_unit_humid_air(self) -> PositiveFloat:
        """Entropy per unit dry air (J/kg humid air.K)"""
        return round(self._get_ha_property("Sha"), 2)

    @property
    def volume_per_unit_dry_air(self) -> PositiveFloat:
        """Volume per unit dry air (m3/kg dry air)"""
        return round(self._get_ha_property("Vda"), 3)

    @property
    def volume_per_unit_humid_air(self) -> PositiveFloat:
        """Volume per unit humid air (m3/kg humid air)"""
        return round(self._get_ha_property("Vha"), 3)

    @property
    def density_per_unit_dry_air(self) -> PositiveFloat:
        """Density per unit dry air (kg/m3)"""
        return round(1 / self._get_ha_property("Vda"), 3)

    @property
    def density_per_unit_humid_air(self) -> PositiveFloat:
        """Density per unit humid air (kg/m3)"""
        return round(1 / self._get_ha_property("Vha"), 3)

    @property
    def thermal_conductivity(self) -> PositiveFloat:
        """Thermal conductivity (W/m.K)"""
        return round(self._get_ha_property("Conductivity"), 4)

    @property
    def dynamic_viscosity(self) -> PositiveFloat:
        """Dynamic viscosity (Pa.s)"""
        return round(self._get_ha_property("Visc"), 8)

    @property
    def kinematic_viscosity_per_unit_dry_air(self) -> PositiveFloat:
        """Kinematic viscosity per unit dry air(m2/s)"""
        density_per_unit_dry_air = 1 / self._get_ha_property("Vda")
        dynamic_viscosity = self._get_ha_property("Visc")
        return round(dynamic_viscosity / density_per_unit_dry_air, 8)

    @property
    def kinematic_viscosity_per_unit_humid_air(self) -> PositiveFloat:
        """Kinematic viscosity per unit dry air(m2/s)"""
        density_per_unit_humid_air = 1 / self._get_ha_property("Vha")
        dynamic_viscosity = self._get_ha_property("Visc")
        return round(dynamic_viscosity / density_per_unit_humid_air, 8)

    @property
    def water_mole_fraction(self) -> PositiveFloat:
        """Water mole fraction mol water/mol humid air"""
        return round(self._get_ha_property("psi_w"), 4)

    @property
    def compressibility_factor(self) -> PositiveFloat:
        """Compressibility factor (Z=pv/RT)"""
        return round(self._get_ha_property("Z"), 4)
