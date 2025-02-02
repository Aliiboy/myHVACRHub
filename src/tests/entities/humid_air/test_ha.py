import unittest

from domain.entities.humid_air.ha_entity import HumidAirEntity


class TestHumidAir(unittest.TestCase):
    def setUp(self) -> None:
        self.humid_air = HumidAirEntity(temp_dry_bulb=20, relative_humidity=50)

    def test_partial_pressure_of_water_vapor(self) -> None:
        self.assertEqual(self.humid_air.partial_pressure_of_water_vapor, 1174.49)

    def test_humidity_ratio(self) -> None:
        self.assertEqual(self.humid_air.humidity_ratio, 0.007294)

    def test_temp_dew_point(self) -> None:
        self.assertEqual(self.humid_air.temp_dew_point, 9.27)

    def test_temp_wet_buld(self) -> None:
        self.assertEqual(self.humid_air.temp_wet_bulb, 13.78)

    def test_enthalpy_per_humid_air(self) -> None:
        self.assertEqual(self.humid_air.enthalpy_per_humid_air, 38343.0)

    def test_specific_heat_per_unit_humid_air(self) -> None:
        self.assertEqual(self.humid_air.specific_heat_per_unit_humid_air, 1012.47)

    def test_entropy_per_unit_humid_air(self) -> None:
        self.assertEqual(self.humid_air.entropy_per_unit_humid_air, 138.96)

    def test_volume_per_unit_humid_air(self) -> None:
        self.assertEqual(self.humid_air.specific_volume_per_unit_humid_air, 0.834)

    def test_density_per_unit_humid_air(self) -> None:
        self.assertEqual(self.humid_air.density_per_unit_humid_air, 1.199)

    def test_thermal_conductivity(self) -> None:
        self.assertEqual(self.humid_air.thermal_conductivity, 0.0259)

    def test_dynamic_viscosity(self) -> None:
        self.assertEqual(self.humid_air.dynamic_viscosity, 1.814e-05)

    def test_prandtl_number(self) -> None:
        self.assertEqual(self.humid_air.prandtl_number, 0.71)

    def test_kinematic_viscosity_per_unit_humid_air(self) -> None:
        self.assertEqual(
            self.humid_air.kinematic_viscosity_per_unit_humid_air, 1.513e-05
        )

    def test_compressibility_factor(self) -> None:
        self.assertEqual(self.humid_air.compressibility_factor, 0.9996)
