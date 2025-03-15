import unittest

from humid_air.domain.entities.humid_air_entity import HumidAirEntity


class TestHumidAirEntity(unittest.TestCase):
    def setUp(self) -> None:
        self.humid_air = HumidAirEntity(temp_dry_bulb=20, relative_humidity=50)

    def test_calculate_partial_pressure_of_water_vapor(self) -> None:
        expected_value: float = 1174.49
        self.assertAlmostEqual(
            self.humid_air.partial_pressure_of_water_vapor, expected_value, places=2
        )

    def test_calculate_humidity_ratio(self) -> None:
        expected_value: float = 0.007294
        self.assertAlmostEqual(self.humid_air.humidity_ratio, expected_value, places=6)

    def test_calculate_dew_point_temperature(self) -> None:
        expected_value: float = 9.27
        self.assertAlmostEqual(self.humid_air.temp_dew_point, expected_value, places=2)

    def test_calculate_wet_bulb_temperature(self) -> None:
        expected_value: float = 13.78
        self.assertAlmostEqual(self.humid_air.temp_wet_bulb, expected_value, places=2)

    def test_calculate_enthalpy_per_unit_humid_air(self) -> None:
        expected_value: float = 38343.0
        self.assertAlmostEqual(
            self.humid_air.enthalpy_per_humid_air, expected_value, places=0
        )

    def test_calculate_specific_heat_per_unit_humid_air(self) -> None:
        expected_value: float = 1012.47
        self.assertAlmostEqual(
            self.humid_air.specific_heat_per_unit_humid_air, expected_value, places=2
        )

    def test_calculate_entropy_per_unit_humid_air(self) -> None:
        expected_value: float = 138.96
        self.assertAlmostEqual(
            self.humid_air.entropy_per_unit_humid_air, expected_value, places=2
        )

    def test_calculate_specific_volume_per_unit_humid_air(self) -> None:
        expected_value: float = 0.834
        self.assertAlmostEqual(
            self.humid_air.specific_volume_per_unit_humid_air, expected_value, places=3
        )

    def test_calculate_density_per_unit_humid_air(self) -> None:
        expected_value: float = 1.199
        self.assertAlmostEqual(
            self.humid_air.density_per_unit_humid_air, expected_value, places=3
        )

    def test_calculate_thermal_conductivity(self) -> None:
        expected_value: float = 0.0259
        self.assertAlmostEqual(
            self.humid_air.thermal_conductivity, expected_value, places=4
        )

    def test_calculate_dynamic_viscosity(self) -> None:
        expected_value: float = 1.814e-05
        self.assertAlmostEqual(
            self.humid_air.dynamic_viscosity, expected_value, places=8
        )

    def test_calculate_kinematic_viscosity_per_unit_humid_air(self) -> None:
        expected_value: float = 1.513e-05
        self.assertAlmostEqual(
            self.humid_air.kinematic_viscosity_per_unit_humid_air,
            expected_value,
            places=8,
        )

    def test_calculate_prandtl_number(self) -> None:
        expected_value: float = 0.71
        self.assertAlmostEqual(self.humid_air.prandtl_number, expected_value, places=2)

    def test_calculate_compressibility_factor(self) -> None:
        expected_value: float = 0.9996
        self.assertAlmostEqual(
            self.humid_air.compressibility_factor, expected_value, places=4
        )
