import logging
from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi.encoders import jsonable_encoder

from app.services.constants import FORMAT, PERMISSIONS_BODY, SPREADSHEET_BODY


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    now_date_time = datetime.now().strftime(FORMAT)
    SPREADSHEET_BODY['properties']['title'] += f'{now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    logging.basicConfig(level=logging.INFO)
    logging.info(f'Table create: '
                 f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in charity_projects:
        project = jsonable_encoder(project)
        new_row = [project['name'], project['close_date'],
                   project['description']]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C1000',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )