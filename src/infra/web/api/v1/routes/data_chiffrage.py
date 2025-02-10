prix_production_froid = [
    {"min": 100, "max": 200, "prix": 20094},
    {"min": 201, "max": 300, "prix": 21972},
    {"min": 301, "max": 400, "prix": 24142},
    {"min": 401, "max": 500, "prix": 28462},
    {"min": 501, "max": 650, "prix": 30971},
    {"min": 651, "max": 800, "prix": 38062},
]


prix_equipement_frigorifere = [
    {"min": 0, "max": 10, "prix": 2700},
    {"min": 11, "max": 20, "prix": 2941},
    {"min": 21, "max": 30, "prix": 3230},
    {"min": 31, "max": 50, "prix": 3516},
    {"min": 51, "max": 75, "prix": 4511},
]

bilan_frigo = {
    "QUAI": [
        {"vol_min": 0, "vol_max": 1900, "ratio": 52},
        {"vol_min": 1901, "vol_max": 3200, "ratio": 41},
        {"vol_min": 3201, "vol_max": 3840, "ratio": 33},
        {"vol_min": 3841, "vol_max": 6400, "ratio": 26},
    ],
    "CF": [
        {"vol_min": 0, "vol_max": 500, "ratio": 28},
        {"vol_min": 501, "vol_max": 800, "ratio": 25},
        {"vol_min": 801, "vol_max": 1100, "ratio": 21},
        {"vol_min": 1101, "vol_max": 1600, "ratio": 24},
        {"vol_min": 1601, "vol_max": 2200, "ratio": 20},
        {"vol_min": 2201, "vol_max": 3000, "ratio": 20},
        {"vol_min": 3001, "vol_max": 4800, "ratio": 20},
        {"vol_min": 4801, "vol_max": 6600, "ratio": 15},
        {"vol_min": 6601, "vol_max": 8000, "ratio": 15},
    ],
    "PLATEFORME": [
        {"vol_min": 0, "vol_max": 1900, "ratio": 40},
        {"vol_min": 1901, "vol_max": 10800, "ratio": 25},
        {"vol_min": 10801, "vol_max": 26400, "ratio": 17},
    ],
}

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
    "CHILLER_TRANE_1234ZE": lambda x: -1.0713e-4 * x**3
    + 0.0611 * x**2
    + 311.7012 * x
    - 29546.7417,
    "CHILLER_CTA_R290": lambda x: -9.9768e-4 * x**3
    + 1.3867 * x**2
    - 382.8699 * x
    + 125355.966,
    "CHILLER_INTERCON_NH3": lambda x: -3.4880e-3 * x**3
    + 4.3789 * x**2
    - 1321.0512 * x
    + 222326.724,
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
