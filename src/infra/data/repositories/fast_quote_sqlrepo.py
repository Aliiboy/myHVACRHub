from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import asc, select

from app.repositories.fast_quote_interface import (
    ColdRoomCoolingCoefficientRepositoryInterface,
)
from domain.entities.fast_quote.cold_room_entity import ColdRoom
from domain.entities.fast_quote.cooling_load_fast_coef_entity import (
    CoolingLoadFastCoefficient,
)
from infra.data.models.cooling_load_fast_coef_sqlmodel import (
    CoolingLoadFastCoefficientSQLModel,
)
from infra.data.sql_unit_of_work import SQLUnitOfWork
from infra.web.dtos.fast_quote_dtos import CoolingLoadFastCoefficientBody


class ColdRoomCoolingCoefficientSQLRepository(
    ColdRoomCoolingCoefficientRepositoryInterface
):
    def __init__(self, unit_of_work: SQLUnitOfWork):
        self.unit_of_work = unit_of_work

    # write
    def add_coefficient(
        self, coefficient: CoolingLoadFastCoefficient
    ) -> CoolingLoadFastCoefficient:
        try:
            with self.unit_of_work as uow:
                query = CoolingLoadFastCoefficientSQLModel(
                    id=coefficient.id,
                    category=coefficient.category,
                    vol_min=coefficient.vol_min,
                    vol_max=coefficient.vol_max,
                    coef=coefficient.coef,
                )
                uow.session.add(query)
                uow.session.flush()
                return query.to_entity()
        except IntegrityError:
            # TODO : à personnaliser ou supprimer..
            raise ValueError("L'ajout de ce coefficient genere une erreur.")

    def update_coefficient(
        self, id: UUID, data: CoolingLoadFastCoefficientBody
    ) -> CoolingLoadFastCoefficient | None:
        with self.unit_of_work as uow:
            coefficient = uow.session.get(CoolingLoadFastCoefficientSQLModel, id)
            if not coefficient:
                return None
            for key, value in data.model_dump().items():
                setattr(coefficient, key, value)
            uow.session.commit()
            return coefficient.to_entity()

    # read
    def get_coef_by_category_and_volume(self, cold_room: ColdRoom) -> int | None:
        with self.unit_of_work as uow:
            query = (
                select(CoolingLoadFastCoefficientSQLModel)
                .where(
                    CoolingLoadFastCoefficientSQLModel.category == cold_room.category
                )
                .where(CoolingLoadFastCoefficientSQLModel.vol_min <= cold_room.volume)
                .where(CoolingLoadFastCoefficientSQLModel.vol_max >= cold_room.volume)
            )
            coefficient = uow.session.exec(query).first()
            return coefficient.coef if coefficient else None

    def get_all_coefficients(self, limit: int) -> list[CoolingLoadFastCoefficient]:
        with self.unit_of_work as uow:
            query = (
                select(CoolingLoadFastCoefficientSQLModel)
                .order_by(
                    asc(CoolingLoadFastCoefficientSQLModel.category),
                    asc(CoolingLoadFastCoefficientSQLModel.vol_min),
                )
                .limit(limit)
            )
            coefficients = uow.session.exec(query).all()
            return [coefficient.to_entity() for coefficient in coefficients]
