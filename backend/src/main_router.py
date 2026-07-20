from fastapi import APIRouter
from src.categories.router import categories_router
from src.products.router import products_router
from src.users.router import users_router
from src.cart.router import cart_router
from src.orders.router import orders_router
from src.media.router import media_router

main_router = APIRouter(prefix="/api")
main_router.include_router(categories_router)
main_router.include_router(products_router)
main_router.include_router(users_router)
main_router.include_router(cart_router)
main_router.include_router(orders_router)
main_router.include_router(media_router)