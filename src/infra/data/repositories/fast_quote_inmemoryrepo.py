import os
from typing import Final

import pandas

from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cold_room_entity import ColdRoom
from infra.web.settings import AppSettings


class ColdRoomCoolingCoefficientExcelRepository(
    ColdRoomCoolingCoefficientRepositoryInterface
):
    settings = AppSettings()
    excel_file: Final[str] = settings.EXCEL_DATABASE_URL
    sheet_name: Final[str] = "ratios"

    def get_coef_by_category_and_volume(self, cold_room: ColdRoom) -> int:
        if not os.path.exists(self.excel_file):
            raise FileNotFoundError(f"Le fichier {self.excel_file} est introuvable.")

        data_frame = pandas.read_excel(
            self.excel_file, sheet_name=self.sheet_name, engine="openpyxl"
        )

        filtered_data_frame = data_frame[data_frame["type"] == cold_room.category.value]

        for _, row in filtered_data_frame.iterrows():
            if row["vol_min"] <= cold_room.volume <= row["vol_max"]:
                return row["ratio"]

        raise ValueError(
            f"Aucun coefficient trouvé pour {cold_room.category.value} avec un volume de {cold_room.volume} m³"
        )
