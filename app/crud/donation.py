from typing import Optional

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase):
    async def create_with_investment(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User
    ) -> Donation:
        from app.services.investment import investing_new_donation
        new_donation = await super().create(obj_in, session, user=user)
        await investing_new_donation(new_donation, session)
        await session.commit()
        await session.refresh(new_donation)
        return new_donation

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
