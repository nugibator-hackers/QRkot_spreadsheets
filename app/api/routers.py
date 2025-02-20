from fastapi import APIRouter
from app.api.endpoints import (
    main_page_router,
    user_router,
    charityproject_router,
    donation_router)


main_router = APIRouter()
main_router.include_router(main_page_router)
main_router.include_router(user_router)
main_router.include_router(
    charityproject_router,
    prefix='/charity_project',
    tags=['Charity Project'])
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Donation'])
