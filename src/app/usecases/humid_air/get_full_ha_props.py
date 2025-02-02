from domain.entities.humid_air.ha_entity import HumidAirEntity


class GetFullHAPropertyUseCase:
    def execute(
        self, pressure: float, temp_dry_bulb: float, relative_humidity: float
    ) -> HumidAirEntity:
        return HumidAirEntity(
            pressure=pressure,
            temp_dry_bulb=temp_dry_bulb,
            relative_humidity=relative_humidity,
        )
