from datetime import datetime
from typing import Optional, List
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
from app.crud.donation import donation_crud  # Добавлен импорт
from app.services.investing import investing_donations_in_projects

class CRUDCharityProject(CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate,]):

    async def create_with_investing(
        self,
        charity_project: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        # Создаем проект
        new_project = await self.create(charity_project, session)
        new_project.set_default()
        # Инвестируем средства
        await self.invest_donations_in_project(new_project, session)
        return new_project

    async def invest_donations_in_project(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> None:
        # Получаем открытые донаты
        donations = await donation_crud.get_not_closed_objects(session)
        # Распределяем средства
        invested_donations = investing_donations_in_projects(project, donations)
        session.add_all(invested_donations)
        await session.commit()
        await session.refresh(project)

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        return (await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )).scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[dict]:
        projects = await session.execute(
            select([
                CharityProject.name,
                CharityProject.description,
                (
                    extract('epoch', CharityProject.close_date) -
                    extract('epoch', CharityProject.create_date)
                ).label('collection_time')
            ]).where(
                CharityProject.fully_invested == True  # noqa
            ).order_by('collection_time')
        )
        return projects.fetchall()

    async def get_not_closed_objects(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        return await super().get_not_closed_objects(session)

    async def create_charity_project(
        self,
        charity_project: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        return await self.create(charity_project, session)
    
    async def update_with_close_check(
        self,
        charity_project: CharityProjectDB,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ):
        charity_project = await self.update_charity_project(
            charity_project, obj_in, session
        )
        if charity_project.invested_amount == charity_project.full_amount:
            setattr(charity_project, 'fully_invested', True)
            setattr(charity_project, 'close_date', datetime.now())
            await session.commit()
            await session.refresh(charity_project)
        return charity_project

    async def update_charity_project(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        return await self.update(db_obj, obj_in, session)

    async def remove_charity_project(
        self,
        db_obj: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        return await self.remove(db_obj, session)

charity_project_crud = CRUDCharityProject(CharityProject)