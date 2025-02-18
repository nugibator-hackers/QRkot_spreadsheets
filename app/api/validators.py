from http import HTTPStatus

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id,
                                                     session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_full_amount_not_less_then_invested(
        db_obj,
        obj_in
):
    obj_data = jsonable_encoder(db_obj)
    if obj_in['full_amount'] < obj_data['invested_amount']:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Требуемая сумма не может быть меньше внесённой!',
        )


async def check_charity_project_is_closed(
        charity_project: CharityProject
):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Удаление закрытых проектов запрещено!'
        )


async def check_charity_project_is_invested(
        charity_project: CharityProject
):
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Запрещено удаление проектов, '
                    'в которые уже внесены средства!')
        )


async def check_charity_project_fields(
        obj_in
):
    if not obj_in:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Попытка присвоить значение нередактируемым полям!'
        )
