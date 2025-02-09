from pydantic import NegativeInt, PositiveFloat, PositiveInt


class HumidAirSettings:
    # pressure
    pressure_description: str = "Pression absolue de l'air en [Pa]"
    pressure_default_value: PositiveFloat = 101325
    pressure_ge: PositiveInt = 10
    pressure_le: PositiveFloat = 1e7

    # dry-bulb temperature
    tdb_description: str = "Température sèche de l'air en [°C]"
    tdb_ge: NegativeInt = -143
    tdb_le: PositiveInt = 350

    # relative humidity
    rh_description: str = "Humidité relative de l'air en [%]"
    rh_ge: PositiveInt = 0
    rh_le: PositiveInt = 100

    # Autres descriptions des propriétés de HumidAir
    partial_pressure_of_water_vapor: str = "Pression de vapeur saturante en [Pa]"
    humidity_ratio_description: str = "Humidité absolue de l'air [kg eau/kg air sec]"
    temp_dew_point_description: str = "Température du point de rosée en [°C]"
    temp_wet_bulb_description: str = "Température bulbe humide en [°C]"
    enthalpy_per_humid_air_description: str = "Enthalpie par kg d'air humide [J/kg]"
    specific_heat_per_unit_humid_air_description: str = (
        "Capacité thermique massique par kg d'air humide [J/kg.K]"
    )
    entropy_per_unit_humid_air_description: str = (
        "Entropie par kg d'air humide [J/kg.K]"
    )
    specific_volume_per_unit_humid_air_description: str = (
        "Volume spécifique par kg d'air humide [m³/kg]"
    )
    density_per_unit_humid_air_description: str = "Densité de l'air humide [kg/m³]"
    thermal_conductivity_description: str = "Conductivité thermique [W/m.K]"
    dynamic_viscosity_description: str = "Viscosité dynamique [Pa.s]"
    kinematic_viscosity_per_unit_humid_air_description: str = (
        "Viscosité cinématique par kg d'air humide [m²/s]"
    )
    prandtl_number_description: str = "Nombre de Prandlt"
    compressibility_factor_description: str = "Facteur de compressibilité [Z=pv/RT]"
