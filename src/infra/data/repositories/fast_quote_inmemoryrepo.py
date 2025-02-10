import os
from typing import Final

import pandas

from app.repositories.fast_quote_interface import FastQuoteRepositoryInterface
from domain.entities.fast_quote.cold_room_entity import ColdRoom

prix_production_froid = [
    {"min": 100, "max": 200, "prix": 43826},
    {"min": 201, "max": 300, "prix": 45844},
    {"min": 301, "max": 400, "prix": 49758},
    {"min": 401, "max": 500, "prix": 54238},
    {"min": 501, "max": 650, "prix": 58995},
    {"min": 651, "max": 800, "prix": 67136},
]


prix_equipement_frigorifere = [
    {"min": 0, "max": 10, "prix": 3730},
    {"min": 11, "max": 20, "prix": 4081},
    {"min": 21, "max": 30, "prix": 4507},
    {"min": 31, "max": 50, "prix": 4986},
    {"min": 51, "max": 75, "prix": 6327},
]

# DT 8
prix_conso_frigorifere = {
    "SF_DA": [
        {"min": 0, "max": 10, "prix": 256},
        {"min": 11, "max": 20, "prix": 190},
        {"min": 21, "max": 30, "prix": 225},
        {"min": 31, "max": 40, "prix": 199},
        {"min": 41, "max": 50, "prix": 191},
        {"min": 51, "max": 60, "prix": 161},
        {"min": 61, "max": 75, "prix": 216},
    ],
    "SF_DE": [
        {"min": 0, "max": 10, "prix": 285},
        {"min": 11, "max": 20, "prix": 208},
        {"min": 21, "max": 30, "prix": 246},
        {"min": 31, "max": 40, "prix": 218},
        {"min": 41, "max": 50, "prix": 211},
        {"min": 51, "max": 60, "prix": 181},
        {"min": 61, "max": 75, "prix": 234},
    ],
    "DF_DA": [
        {"min": 0, "max": 10, "prix": 452},
        {"min": 11, "max": 20, "prix": 338},
        {"min": 21, "max": 30, "prix": 263},
        {"min": 31, "max": 40, "prix": 270},
        {"min": 41, "max": 50, "prix": 275},
        {"min": 51, "max": 60, "prix": 295},
    ],
    "DF_DE": [
        {"min": 0, "max": 10, "prix": 499},
        {"min": 11, "max": 20, "prix": 378},
        {"min": 21, "max": 30, "prix": 285},
        {"min": 31, "max": 40, "prix": 291},
        {"min": 41, "max": 50, "prix": 296},
        {"min": 51, "max": 60, "prix": 313},
    ],
}


formules_prix_modele_frigorifere = {
    "CHILLER_TRANE_1234ZE": lambda x: -2e-06 * x**4
    + 0.004 * x**3
    - 2.3568 * x**2
    + 682.05 * x
    + 27916,
    "CHILLER_CTA_R290": lambda x: 0.1998 * x**2 + 54.238 * x + 78600,
    "CHILLER_INTERCON_NH3": lambda x: 427.7 * x - 2726.6,
}


facteur_debit_puissance_tuyauterie = 0.238


debit_dn_table = [
    {"de_min": 0, "de_max": 4.7, "dn": 20},
    {"de_min": 4.7, "de_max": 9.3, "dn": 25},
    {"de_min": 9.3, "de_max": 18.3, "dn": 32},
    {"de_min": 18.3, "de_max": 27, "dn": 40},
    {"de_min": 27, "de_max": 51, "dn": 50},
    {"de_min": 51, "de_max": 99, "dn": 65},
    {"de_min": 99, "de_max": 154, "dn": 80},
    {"de_min": 154, "de_max": 312, "dn": 100},
    {"de_min": 312, "de_max": 537, "dn": 125},
    {"de_min": 537, "de_max": 850, "dn": 150},
    {"de_min": 850, "de_max": 1600, "dn": 200},
]


tuyauterie_prix_par_dn = {
    10: 72,
    15: 74,
    20: 81,
    25: 88,
    32: 100,
    40: 114,
    50: 129,
    65: 152,
    80: 172,
    100: 206,
    125: 256,
    150: 299,
    200: 426,
    250: 576,
    300: 705,
}


montant_fixe_mes = 800
montant_fixe_divers = 500

proportion_mes = 0.015
proportion_chef_chantier = 0.03
proportion_frais_divers = 0.01


class FastQuoteInMemoryRepository(FastQuoteRepositoryInterface):
    excel_file: Final[str] = "src/infra/data/repositories/database.xlsx"
    sheet_name: Final[str] = "ratios"

    def get_cooling_load_fast_coefficient(self, cold_room: ColdRoom) -> int:
        if not os.path.exists(self.excel_file):
            raise FileNotFoundError(f"Le fichier {self.excel_file} est introuvable.")

        data_frame = pandas.read_excel(
            self.excel_file, sheet_name=self.sheet_name, engine="openpyxl"
        )

        filtered_data_frame = data_frame[data_frame["type"] == cold_room.type.value]

        for _, row in filtered_data_frame.iterrows():
            if row["vol_min"] <= cold_room.volume <= row["vol_max"]:
                return row["ratio"]

        raise ValueError(
            f"Aucun coefficient trouvé pour {cold_room.type.value} avec un volume de {cold_room.volume} m³"
        )
