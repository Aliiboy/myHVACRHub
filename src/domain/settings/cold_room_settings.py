from pydantic import PositiveInt


class ColdRoomSettings:
    # length
    length_description: str = "Longueur totale de la chambre froide en [m]"
    length_ge: PositiveInt = 1
    length_le: PositiveInt = 500
    # width
    width_description: str = "Largeur totale de la chambre froide en [m]"
    width_ge: PositiveInt = 1
    width_le: PositiveInt = 500
    # height
    height_description: str = "Hauteur totale de la chambre froide en [m]"
    height_ge: PositiveInt = 1
    height_le: PositiveInt = 500
    # type
    type_description: str = "Type de chambre froide"
    # volume
    volume_description: str = "Volume total de la chambre froide en [m³]"
