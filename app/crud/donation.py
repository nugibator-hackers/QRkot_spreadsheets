from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
    DonationUpdate
]):
    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ):
        """Получает все пожертвования для конкретного пользователя."""
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()

    async def create(
            self,
            obj_in: DonationCreate,
            session: AsyncSession,
            user: User,
            make_commit: bool = True,
    ):
        """Создает новое пожертвование."""
        db_obj = Donation(
            **obj_in.dict(),
            user_id=user.id
        )
        session.add(db_obj)
        if make_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_multi(
            self,
            session: AsyncSession,
    ):
        """Получает все пожертвования."""
        donations = await session.execute(select(Donation))
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)