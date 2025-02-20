from typing import Optional

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> list[Donation]:
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id))
        return reservations.scalars().all()

    async def get_oldest_open_donation(
            self, session: AsyncSession,
    ) -> Optional[Donation]:
        oldest_open_donation = await session.execute(
            select(Donation).filter(
                Donation.fully_invested.is_(False))
            .order_by(asc(Donation.create_date))
            .limit(1))
        return oldest_open_donation.scalars().first()


donation_crud = CRUDDonation(Donation)
