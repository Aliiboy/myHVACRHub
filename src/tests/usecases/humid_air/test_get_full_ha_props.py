import unittest

from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from domain.entities.humid_air.ha_entity import HumidAirEntity


class TestGetFullHAPropertyUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.use_case = GetFullHAPropertyUseCase()

    def test_execute_returns_humid_air_object(self) -> None:
        # given
        pressure = 101325
        temp_dry_bulb = 25.0
        relative_humidity = 0.5

        # when
        humid_air = self.use_case.execute(
            pressure=pressure,
            temp_dry_bulb=temp_dry_bulb,
            relative_humidity=relative_humidity,
        )

        # then
        self.assertIsInstance(humid_air, HumidAirEntity)
        self.assertEqual(humid_air.temp_dry_bulb, temp_dry_bulb)
        self.assertEqual(humid_air.relative_humidity, relative_humidity)
