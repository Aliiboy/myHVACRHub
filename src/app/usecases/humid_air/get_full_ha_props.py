from domain.entities.humid_air.ha_entity import HumidAir


class GetFullHAPropertyUseCase:
    def execute(self, temp_dry_bulb: float, relative_humidity: float) -> HumidAir:
        return HumidAir(
            temp_dry_bulb=temp_dry_bulb, relative_humidity=relative_humidity
        )
