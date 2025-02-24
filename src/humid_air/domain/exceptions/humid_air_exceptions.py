from pydantic_core import ErrorDetails


class HumidAirValidationException(Exception):
    def __init__(self, errors: list[ErrorDetails]):
        self.errors = [
            {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
            for err in errors
        ]
        super().__init__("HumidAirValidationException")
