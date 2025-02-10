import math
from collections.abc import Callable
from http import HTTPStatus
from typing import cast

from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify
from flask_jwt_extended import jwt_required
from flask_openapi3 import APIBlueprint, Tag  # type: ignore[attr-defined]

from app.usecases.fast_quote.add_cooling_load_fast_coefficient import (
    AddCoolingLoadFastCoefficientUseCase,
)
from app.usecases.fast_quote.calc_cold_room_cooling_load_fast import (
    CalculateColdRoomCoolingLoadFastUseCase,
)
from infra.web.api.v1.routes.fast_quote_controllers import *
from infra.web.container import AppContainer
from infra.web.decorators.role_required import role_required
from infra.web.dtos.fast_quote_dtos import (
    AddCoolingLoadFastCoefficientRequest,
    ColdRoomRequest,
    ColdRoomResponse,
    GroupeFroidRequest,
    LocalFrigoRequest,
    PrixTotal,
    TuyauterieRequest,
)
from infra.web.dtos.generic import ClientErrorResponse, SuccessResponse

tag = Tag(name="Chiffrage rapide", description="Genere un chiffrage rapide")

security = [{"jwt": []}]  # type: ignore[var-annotated]

router = APIBlueprint(
    "/fast_quote",
    __name__,
    url_prefix="/fast_quote",
    abp_tags=[tag],
    doc_ui=True,
)


@router.post(
    "/add_cooling_load_coefficient",
    description="Ajoute un coefficient de charge frigorifique",
    responses={
        HTTPStatus.CREATED: SuccessResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ClientErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@cast("Callable[..., Response]", role_required("moderator", "admin"))
@inject
def add_cooling_load_coefficient(
    body: AddCoolingLoadFastCoefficientRequest,
    use_case: AddCoolingLoadFastCoefficientUseCase = Provide[
        AppContainer.add_cooling_load_fast_coefficient_usecase
    ],
) -> Response:
    try:
        use_case.execute(
            category=body.category,
            vol_min=body.vol_min,
            vol_max=body.vol_max,
            coef=body.coef,
        )
        return SuccessResponse(
            code=HTTPStatus.CREATED,
            message="Coefficient ajouté avec succès",
        ).to_response()
    except ValueError as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


@router.get(
    "calculate_cold_room_cooling_load_fast",
    description="Determine la puissance frigorifique d'une chambre froide (au ratio)",
    security=security,
    responses={
        HTTPStatus.OK: ColdRoomResponse,
        HTTPStatus.UNAUTHORIZED: ClientErrorResponse,
        HTTPStatus.UNPROCESSABLE_ENTITY: ClientErrorResponse,
    },
)
@cast("Callable[..., Response]", jwt_required())
@inject
def calculate_cold_room_cooling_load_fast(
    query: ColdRoomRequest,
    use_case: CalculateColdRoomCoolingLoadFastUseCase = Provide[
        AppContainer.calculate_cold_room_cooling_load_fast_usecase
    ],
) -> Response:
    try:
        cold_room, cold_room_power = use_case.execute(
            query.length, query.width, query.height, query.type
        )

        return ColdRoomResponse.from_use_case_result(
            cold_room, cold_room_power
        ).to_response()
    except ValueError as e:
        return ClientErrorResponse(
            code=HTTPStatus.UNPROCESSABLE_ENTITY, message=str(e)
        ).to_response()


# ======= ROUTE =========


@router.get(
    "/prix_frigo_local",
    security=security,
)
@cast("Callable[..., Response]", jwt_required())
def calculate_prix_frigo_local(query: LocalFrigoRequest):
    # On calcule ensuite la puissance unitaire de chaque appareil en kW
    puissance_unitaire_appareils = math.ceil(
        query.puissance_frigo_local / query.nb_appareils
    )

    # On calcule le prix de consommation des frigorifères
    prix_conso_frigorifere_unitaire = calculer_prix_conso_frigorifere(
        puissance_unitaire_appareils, query.type_diffusion, query.type_degivrage
    )
    prix_total_conso_frigorifere = query.nb_appareils * prix_conso_frigorifere_unitaire

    # On calcule le prix des équipements des appareils
    prix_equipement_frigorifere_unitaire = calculer_prix_equipement_frigorigere(
        puissance_unitaire_appareils
    )
    prix_total_equipement_frigorifere = (
        query.nb_appareils * prix_equipement_frigorifere_unitaire
    )

    # On calcule le prix total final pour le local en terme de froid
    prix_total_final = prix_total_conso_frigorifere + prix_total_equipement_frigorifere

    return jsonify(
        {
            "puissance_unitaire_appareil": puissance_unitaire_appareils,
            "prix_total_conso_frigorifere": prix_total_conso_frigorifere,
            "prix_total_equipement": prix_total_equipement_frigorifere,
            "prix_total_final": prix_total_final,
        }
    )


@router.get(
    "/prix_groupe_froid",
    security=security,
)
@cast("Callable[..., Response]", jwt_required())
def calculate_prix_groupe_froid(query: GroupeFroidRequest):
    prix_prod_froid = calculer_prix_puissance_frigo(query.puissance_bilan_thermique)
    prix_groupe_froid = calculer_prix_groupe_froid(
        query.puissance_bilan_thermique, query.modele_GF
    )

    return jsonify(
        {"prix_groupe_froid": prix_groupe_froid, "prix_prod_froid": prix_prod_froid}
    )


@router.get(
    "/prix_tuyauterie",
    security=security,
)
@cast("Callable[..., Response]", jwt_required())
def calculate_prix_tuyauterie(query: TuyauterieRequest):
    # Calcul du débit min et max selon la puissance
    debitMin, debitMax = calculer_debit_min_max(query.p_min, query.p_max)

    # Calcul du diamètre nominal selon le débit min et max
    DNmin, DNmax = calculer_dn_min_max(debitMin, debitMax)

    # Calcul du prix selon le DN et la longueur de tuyau
    prixLongueurMin, prixLongueurMax = calculer_prix_longueur_min_max(
        DNmin, DNmax, query.longueur_aller * 2
    )

    # Calcul du prix moyen
    prixMoyen = (prixLongueurMax + prixLongueurMin) / 2
    prixMoyenFinal = prixMoyen

    # Calcul du prix moyen pondéré par difficulté (s'il y en a)
    if query.difficulte != 0:
        prixMoyenFinal += prixMoyen * query.difficulte

    return jsonify(
        {
            "debitMin": debitMin,
            "debitMax": debitMax,
            "DNmin": DNmin,
            "DNmax": DNmax,
            "prixLongueurMin": prixLongueurMin,
            "prixLongueurMax": prixLongueurMax,
            "prixMoyen": prixMoyen,
            "prixMoyenFinal": prixMoyenFinal,
        }
    )


@router.get(
    "/prix_elec_autom",
    security=security,
)
@cast("Callable[..., Response]", jwt_required())
def calculate_prix_elec_autom(query: PrixTotal):
    prix_elec_autom = query.prix_total * 0.1

    return jsonify(
        {
            "prix_elec_autom": prix_elec_autom,
        }
    )


@router.get(
    "/prix_frais_divers",
    security=security,
)
@cast("Callable[..., Response]", jwt_required())
def calculate_prix_frais_divers(query: PrixTotal):
    frais_mes, frais_chefChantier, frais_divers = calculer_frais_divers(
        query.prix_total
    )

    return jsonify(
        {
            "frais_mes": frais_mes,
            "frais_chefChantier": frais_chefChantier,
            "frais_divers": frais_divers,
        }
    )
