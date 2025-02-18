from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_fields,
                                check_charity_project_is_closed,
                                check_charity_project_is_invested,
                                check_full_amount_not_less_then_invested,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)]
             )
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await investing(charity_project, Donation, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    obj_in = obj_in.dict(exclude_unset=True)
    await check_charity_project_fields(obj_in)
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_charity_project_is_closed(charity_project)
    if 'name' in obj_in:
        await check_name_duplicate(obj_in['name'], session)
    if 'full_amount' in obj_in:
        await check_full_amount_not_less_then_invested(
            charity_project, obj_in
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    await check_charity_project_is_closed(charity_project)
    await check_charity_project_is_invested(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project