from pydantic import NegativeInt, PositiveFloat, PositiveInt


class HumidAirSettings:
    # pressure
    pressure_default_value: PositiveFloat = 101325
    pressure_description: str = "Pression de l'air en [Pa]"

    # dry-bulb temperature
    tdb_description: str = "Température sèche de l'air en [°C]"
    tdb_ge: NegativeInt = -143
    tdb_le: PositiveInt = 350

    # relative humidity
    rh_description: str = "Humidité relative de l'air en [%]"
    rh_ge: PositiveInt = 0
    rh_le: PositiveInt = 1

    # Autres descriptions des propriétés de HumidAir
    humidity_ratio_description: str = "Humidité absolue de l'air [kg eau/kg air sec]"
    temp_dew_point_description: str = "Température du point de rosée en [°C]"
    temp_wet_bulb_description: str = "Température bulbe humide en [°C]"
    enthalpy_per_dry_air_description: str = "Enthalpie par kg d'air sec [J/kg]"
    enthalpy_per_humid_air_description: str = "Enthalpie par kg d'air humide [J/kg]"
    specific_heat_per_unit_dry_air_description: str = (
        "Capacité thermique massique par kg d'air sec [J/kg.K]"
    )
    specific_heat_per_unit_humid_air_description: str = (
        "Capacité thermique massique par kg d'air humide [J/kg.K]"
    )
    specific_heat_at_constant_volume_per_unit_dry_air_description: str = (
        "Capacité thermique massique à volume constant par kg d'air sec [J/kg.K]"
    )
    specific_heat_at_constant_volume_per_unit_humid_air_description: str = (
        "Capacité thermique massique à volume constant par kg d'air humide [J/kg.K]"
    )
    entropy_per_unit_dry_air_description: str = "Entropie par kg d'air sec [J/kg.K]"
    entropy_per_unit_humid_air_description: str = (
        "Entropie par kg d'air humide [J/kg.K]"
    )
    volume_per_unit_dry_air_description: str = "Volume par kg d'air sec [m³/kg]"
    volume_per_unit_humid_air_description: str = "Volume par kg d'air humide [m³/kg]"
    density_per_unit_dry_air_description: str = "Densité de l'air sec [kg/m³]"
    density_per_unit_humid_air_description: str = "Densité de l'air humide [kg/m³]"
    thermal_conductivity_description: str = "Conductivité thermique [W/m.K]"
    dynamic_viscosity_description: str = "Viscosité dynamique [Pa.s]"
    kinematic_viscosity_per_unit_dry_air_description: str = (
        "Viscosité cinématique par kg d'air sec [m²/s]"
    )
    kinematic_viscosity_per_unit_humid_air_description: str = (
        "Viscosité cinématique par kg d'air humide [m²/s]"
    )
    water_mole_fraction_description: str = (
        "Fraction molaire de l'eau [mol eau/mol air humide]"
    )
    compressibility_factor_description: str = "Facteur de compressibilité [Z=pv/RT]"
