from typing import Optional

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectCreate


class CRUDCharityProject(CRUDBase):
    async def create_with_investment(
        self,
        obj_in: CharityProjectCreate,
        session: AsyncSession
    ) -> CharityProject:
        from app.services.investment import investing_to_new_project
        new_project = await self.create(obj_in, session)
        await investing_to_new_project(new_project, session)
        await session.commit()
        await session.refresh(new_project)
        return new_project

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_oldest_open_project(
            self, session: AsyncSession,
    ) -> Optional[CharityProject]:
        oldest_open_project = await session.execute(
            select(CharityProject).filter(
                CharityProject.fully_invested.is_(False))
            .order_by(asc(CharityProject.create_date))
            .limit(1))
        return oldest_open_project.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
