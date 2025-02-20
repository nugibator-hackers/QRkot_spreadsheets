from fastapi import APIRouter, Response

router = APIRouter(tags=['dev'])


@router.get('/')
def start_page_redirect():
    return Response(status_code=200, media_type="text/html")
