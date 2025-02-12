from domain.entities.humid_air.humid_air_entity import HumidAirEntity


class GetFullHAPropertyUseCase:
    # TODO : change request
    def execute(
        self, pressure: float, temp_dry_bulb: float, relative_humidity: float
    ) -> HumidAirEntity:
        return HumidAirEntity(
            pressure=pressure,
            temp_dry_bulb=temp_dry_bulb,
            relative_humidity=relative_humidity,
        )
