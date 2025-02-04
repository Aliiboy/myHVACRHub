import pytest
from pydantic import ValidationError

from domain.value_objects.dimension_valueobject import Dimension


class TestDimension:
    def test_volume_normal_values(self) -> None:
        valid_dimension = Dimension(thickness=2, width=3, height=4)
        assert valid_dimension.get_volume == 24.0

    def test_volume_zero_and_negative_values(self) -> None:
        with pytest.raises(ValidationError):
            Dimension(thickness=0, width=-3, height=5)

    def test_volume_large_values(self) -> None:
        with pytest.raises(ValidationError):
            Dimension(thickness=1, width=1, height=100000)
