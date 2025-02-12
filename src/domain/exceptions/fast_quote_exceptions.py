from uuid import UUID

# class CoolingLoadFastCoefficientAlreadyExist(Exception):
#     def __init__(self, )


class CoolingLoadFastCoefficientNotFoundException(Exception):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Le coefficient  '{id}' n'existe pas.")
