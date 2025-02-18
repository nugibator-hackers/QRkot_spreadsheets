from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationMe
from app.services.investing import investing

router = APIRouter()


@router.post('/', response_model=DonationMe)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donation = await investing(donation, CharityProject, session)
    new_donation = await donation_crud.create(
        donation, session, user
    )
    return new_donation


@router.get('/',
            response_model=list[DonationDB],
            dependencies=[Depends(current_superuser)]
            )
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationMe],
    response_model_exclude={'close_date', 'fully_invested',
                            'invested_amount', 'user_id'}
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
