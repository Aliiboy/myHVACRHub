from pydantic import ValidationError

from humid_air.app.schemas.get_ha_props_schema import GetHumidAirPropertySchema
from humid_air.domain.entities.humid_air_entity import HumidAirEntity
from humid_air.domain.exceptions.humid_air_exceptions import HumidAirValidationException


class GetHumidAirPropertyUseCase:
    def execute(self, schema: GetHumidAirPropertySchema) -> HumidAirEntity:
        try:
            return HumidAirEntity(
                pressure=schema.pressure,
                temp_dry_bulb=schema.temp_dry_bulb,
                relative_humidity=schema.relative_humidity,
            )
        except ValidationError as e:
            raise HumidAirValidationException(e.errors())
