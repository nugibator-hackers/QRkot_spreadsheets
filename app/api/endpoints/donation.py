from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationDBSuperuser)
from app.crud.donation import donation_crud
from app.core.user import current_user
from app.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.create_with_investment(
        obj_in=donation,
        session=session,
        user=user
    )


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(user=user, session=session)


@router.get('/',
            response_model=list[DonationDBSuperuser],
            dependencies=[Depends(current_superuser)], )
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)
