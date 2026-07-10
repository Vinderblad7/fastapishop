from fastapi import APIRouter
from src.categories.router import categories_router

main_router = APIRouter(prefix="/api")
main_router.include_router(categories_router)
