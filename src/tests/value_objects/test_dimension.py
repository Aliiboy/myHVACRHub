import pytest
from pydantic import ValidationError

from domain.value_objects.dimension_valueobject import Dimension


class TestDimension:
    # === volume ===
    def test_volume_normal_values(self) -> None:
        # given when
        valid_dimension = Dimension(thickness=2, width=3, height=4)
        # then
        assert valid_dimension.get_volume == 24.0

    def test_volume_zero_and_negative_values(self) -> None:
        # given when/then
        with pytest.raises(ValidationError):
            Dimension(thickness=0, width=-3, height=5)

    def test_volume_large_values(self) -> None:
        # given when/then
        with pytest.raises(ValidationError):
            Dimension(thickness=1, width=1, height=100000)
