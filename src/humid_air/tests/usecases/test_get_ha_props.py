import unittest

from humid_air.app.schemas.get_ha_props_schema import GetHumidAirPropertySchema
from humid_air.app.usecases.get_ha_props import GetHumidAirPropertyUseCase
from humid_air.domain.exceptions.humid_air_exceptions import HumidAirValidationException


class TestGetFullHAPropertyUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.use_case = GetHumidAirPropertyUseCase()

    def test_get_full_ha_props_success(self) -> None:
        humid_air_schema = GetHumidAirPropertySchema(
            pressure=101325, temp_dry_bulb=25, relative_humidity=50
        )
        humid_air_entity = self.use_case.execute(humid_air_schema)
        self.assertEqual(humid_air_entity.temp_dry_bulb, humid_air_schema.temp_dry_bulb)
        self.assertEqual(
            humid_air_entity.relative_humidity, humid_air_schema.relative_humidity
        )

    def test_get_full_ha_props_with_exception(self) -> None:
        invalid_humid_air_schema = GetHumidAirPropertySchema(
            pressure=101325, temp_dry_bulb=360, relative_humidity=110
        )
        with self.assertRaises(HumidAirValidationException) as context:
            self.use_case.execute(invalid_humid_air_schema)

        self.assertIsInstance(context.exception, HumidAirValidationException)
        self.assertTrue(len(context.exception.errors) > 0)
        self.assertEqual(context.exception.errors[0]["field"], "temp_dry_bulb")
        self.assertEqual(context.exception.errors[1]["field"], "relative_humidity")
