from infra.web.api.v1.routes.data_chiffrage import *


def calculer_prix_puissance_frigo(puissance_local):
    for plage in prix_production_froid:
        if plage["min"] <= puissance_local <= plage["max"]:
            return plage["prix"]

    # Si aucune plage ne correspond
    return None


def calculer_prix_equipement_frigorigere(puissance_unitaire):
    for plage in prix_equipement_frigorifere:
        if plage["min"] <= puissance_unitaire <= plage["max"]:
            return plage["prix"]

    # Si aucune plage ne correspond
    return None


def calculer_prix_conso_frigorifere(puissance_unitaire, type_flux, type_degivrage):
    cle = f"{type_flux}_{type_degivrage}"
    if cle in prix_conso_frigorifere:
        for plage in prix_conso_frigorifere[cle]:
            if plage["min"] <= puissance_unitaire <= plage["max"]:
                return plage["prix"] * puissance_unitaire

    # Si aucune plage ne correspond
    return None


def calculer_prix_groupe_froid(puissance_unitaire, modele):
    if modele in formules_prix_modele_frigorifere:
        return formules_prix_modele_frigorifere[modele](puissance_unitaire)
    return None


def calculer_debit_min_max(Pmin, Pmax):
    debitMin = Pmin * facteur_debit_puissance_tuyauterie
    debitMax = Pmax * facteur_debit_puissance_tuyauterie

    return debitMin, debitMax


def calculer_dn_min_max(debitMin, debitMax):
    dn_min, dn_max = None, None

    for row in debit_dn_table:
        if dn_min is None and row["de_min"] < debitMin <= row["de_max"]:
            dn_min = row["dn"]
        if dn_max is None and row["de_min"] < debitMax <= row["de_max"]:
            dn_max = row["dn"]

        if dn_min is not None and dn_max is not None:
            break

    return dn_min, dn_max


def calculer_prix_longueur_min_max(dn_min, dn_max, longueur):
    prix_min = tuyauterie_prix_par_dn.get(dn_min, 0) * longueur
    prix_max = tuyauterie_prix_par_dn.get(dn_max, 0) * longueur

    return prix_min, prix_max


def calculer_frais_divers(prix_total):
    frais_mes = montant_fixe_mes + (prix_total * proportion_mes)
    frais_chef_chantier = prix_total * proportion_chef_chantier
    frais_divers = montant_fixe_divers + (prix_total * proportion_frais_divers)

    return frais_mes, frais_chef_chantier, frais_divers


def calculer_volume_chambre(longueur, largeur, hauteur):
    """Calcule le volume d'une chambre froide en m³."""
    return longueur * largeur * hauteur


def calculer_puissance_frigorifique(volume, type_chambre):
    """Calcule la puissance frigorifique en fonction du volume et du type de chambre froide."""
    if type_chambre in bilan_frigo:
        for plage in bilan_frigo[type_chambre]:
            if plage["vol_min"] <= volume <= plage["vol_max"]:
                return volume * plage["ratio"]
    return None  # Si aucun ratio ne correspond
