import unittest

from app.usecases.humid_air.get_full_ha_props import GetFullHAPropertyUseCase
from domain.entities.humid_air.ha_entity import HumidAirEntity


class GetFullHAPropertyUseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.use_case = GetFullHAPropertyUseCase()

    def test_execute_returns_valid_humid_air_entity(self) -> None:
        pressure: float = 101325
        temperature_dry_bulb: float = 25.0
        relative_humidity: float = 0.5
        humid_air_entity: HumidAirEntity = self.use_case.execute(
            pressure=pressure,
            temp_dry_bulb=temperature_dry_bulb,
            relative_humidity=relative_humidity,
        )
        self.assertIsInstance(humid_air_entity, HumidAirEntity)
        self.assertEqual(humid_air_entity.temp_dry_bulb, temperature_dry_bulb)
        self.assertEqual(humid_air_entity.relative_humidity, relative_humidity)
