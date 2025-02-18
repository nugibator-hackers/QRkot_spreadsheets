from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

FALSE = 0


async def get_not_closed_objects(data_base, session):
    not_closed_objects = await session.execute(select(data_base).where(
        data_base.fully_invested == FALSE))
    not_closed_objects = not_closed_objects.scalars().all()
    return not_closed_objects


def prepare_to_close_new_object(new_object):
    new_object['invested_amount'] = new_object['full_amount']
    new_object['fully_invested'] = True
    new_object['close_date'] = datetime.utcnow()
    return new_object


def prepare_to_close_db_object(obj_data, db_object):
    update_db_object = {'invested_amount': obj_data['full_amount'],
                        'fully_invested': True,
                        'close_date': datetime.utcnow()}
    for field in obj_data:
        if field in update_db_object:
            setattr(db_object, field, update_db_object[field])
    return db_object


async def update_db_object(
        sum_to_close_new_object,
        sum_to_close_db_object,
        obj_data,
        db_object,
        session
):
    update_object = {'invested_amount':
                     (sum_to_close_new_object +
                      obj_data['invested_amount'])}
    if sum_to_close_new_object == sum_to_close_db_object:
        update_object['fully_invested'] = True
        update_object['close_date'] = datetime.utcnow()
    for field in obj_data:
        if field in update_object:
            setattr(db_object, field, update_object[field])
    session.add(db_object)
    await session.commit()
    await session.refresh(db_object)


async def investing(
        new_object,
        data_base,
        session: AsyncSession
):
    new_object = new_object.dict()
    not_closed_objects = await get_not_closed_objects(data_base, session)
    if not_closed_objects:
        new_object['invested_amount'] = 0
        sum_to_close_new_object = new_object['full_amount']
        for db_object in not_closed_objects:
            obj_data = jsonable_encoder(db_object)
            sum_to_close_db_object = (obj_data['full_amount'] -
                                      obj_data['invested_amount'])
            if sum_to_close_new_object <= sum_to_close_db_object:
                await update_db_object(
                    sum_to_close_new_object,
                    sum_to_close_db_object,
                    obj_data,
                    db_object,
                    session
                )
                return prepare_to_close_new_object(new_object)
            if sum_to_close_new_object > sum_to_close_db_object:
                new_object['invested_amount'] += sum_to_close_db_object
                sum_to_close_new_object -= sum_to_close_db_object
                session.add(prepare_to_close_db_object(obj_data, db_object))
        await session.commit()
        await session.refresh(db_object)
    return new_object