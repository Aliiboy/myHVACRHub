from pydantic import BaseModel


class GetHumidAirPropertySchema(BaseModel):
    pressure: float
    temp_dry_bulb: float
    relative_humidity: float
