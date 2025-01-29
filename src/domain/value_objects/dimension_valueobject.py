from pydantic import BaseModel, Field, PositiveFloat


class Dimension(BaseModel):
    width: PositiveFloat = Field(le=1e4)
    height: PositiveFloat = Field(le=1e4)
    thickness: PositiveFloat = Field(le=1e4)

    @property
    def get_volume(self) -> float:
        return (self.thickness) * (self.width) * (self.height)
