from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт от ',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}