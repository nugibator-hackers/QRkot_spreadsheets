from aiogoogle import Aiogoogle
from pydantic import BaseModel, validator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (NAME_DUPLICATE,
                           PROJECT_NOT_FOUND,
                           PROJECT_IS_CLOSED,
                           PROJECT_HAS_DONATIONS,
                           FULL_AMOUNT_LESS_INVESTED_AMOUNT)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.services.google_api import spreadsheets_update_value


class GetReportRequest(BaseModel):
    session: AsyncSession
    wrapper_services: Aiogoogle

    class Config:
        arbitrary_types_allowed = True

    @validator('session')
    def session_must_be_valid(cls, v):
        if not v:
            raise ValueError('Session must be valid')
        return v

    @validator('wrapper_services')
    def wrapper_services_must_be_valid(cls, v):
        if not v:
            raise ValueError('Wrapper services must be valid')
        return v


async def get_report(
    request: GetReportRequest = Depends(),
):
    try:
        await spreadsheets_update_value
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(error))
    return spreadsheets_url


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    if await charity_project_crud.get_project_id_by_name(
        project_name, session
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_DUPLICATE,
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return charity_project


async def check_charity_project_not_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_IS_CLOSED
        )


async def check_donations_exists(
    project_id: int,
    session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_HAS_DONATIONS
        )


async def check_new_full_amount_more_invested_amount(
    project_id: int,
    new_full_amount: int,
    session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FULL_AMOUNT_LESS_INVESTED_AMOUNT
        )
