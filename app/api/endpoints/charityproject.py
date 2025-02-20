from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charityproject_exists,
    check_close_project,
    check_full_amount,
    check_name_duplicate,
    check_project_before_edit,
    check_project_invested_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)]
             )
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    return await charityproject_crud.create_with_investment(project, session)


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charityproject_crud.get_multi(session)


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
    charityproject_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charityproject_exists(charityproject_id, session)
    check_project_before_edit(obj_in)
    check_close_project(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(obj_in.full_amount, charityproject_id, session)
    return await charityproject_crud.update(project, obj_in, session)


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session), ):
    project = await check_charityproject_exists(
        charityproject_id, session
    )
    project = await charityproject_crud.remove(project, session)
    check_close_project(project)
    check_project_invested_amount(project)
    return project
