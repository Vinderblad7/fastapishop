from fastapi import APIRouter
from src.categories.router import categories_router
from src.products.router import products_router

main_router = APIRouter(prefix="/api")
main_router.include_router(categories_router)
main_router.include_router(products_router)