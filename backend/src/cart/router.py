from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.dependencies import SessionDep, CurrentUserDep
from src.cart.models import CartModel  
from src.cart.schemas import CartAddSchema, CartResponseSchema, CartUpdateSchema

from src.database import get_redis
from redis.asyncio import Redis
from src.cart.service import get_cart_cache_key
import json

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.post("", response_model=CartResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    data: CartAddSchema, 
    session: SessionDep, 
    current_user: CurrentUserDep,
    redis: Redis = Depends(get_redis)
):  
    query = await session.execute(
        select(CartModel).where(
            CartModel.user_id == current_user.id,
            CartModel.product_id == data.product_id
        )
    )
    existing_item = query.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += data.quantity
        cart_item = existing_item
    else:
        new_item = CartModel(
            user_id=current_user.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        session.add(new_item)
        cart_item = new_item

    await session.commit()

    cache_key = get_cart_cache_key(current_user.id)
    await redis.delete(cache_key)

    result = await session.execute(
        select(CartModel)
        .options(joinedload(CartModel.products))
        .where(CartModel.id == cart_item.id)
    )
    cart_item = result.scalar_one()
    
    return cart_item

@cart_router.get("", response_model=list[CartResponseSchema])
async def get_my_cart(
    session: SessionDep, 
    current_user: CurrentUserDep,
    redis: Redis = Depends(get_redis)
):  
    cache_key = get_cart_cache_key(current_user.id)
    
    cached_cart = await redis.get(cache_key)

    if cached_cart:
        return json.loads(cached_cart)

    print("--> [DEBUG] Cache MISS! Querying DB...")

    query = await session.execute(
        select(CartModel)
        .options(joinedload(CartModel.products))
        .where(CartModel.user_id == current_user.id)
    )
    cart_items = query.scalars().all()

    cart_data = [
        {
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "products": {
                "id": item.products.id,
                "name": item.products.name,
                "description": item.products.description,
                "price": item.products.price,
                "image_url": item.products.image_url,
                "category_id": item.products.category_id,
                "created_at": item.products.created_at.isoformat(),
                "updated_at": item.products.updated_at.isoformat(),
            } if item.products else None,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        }
        for item in cart_items
    ]

    await redis.set(cache_key, json.dumps(cart_data), ex=300)

    return cart_data

@cart_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    session: SessionDep, 
    current_user: CurrentUserDep,
    redis: Redis = Depends(get_redis)
):
    query = await session.execute(
        select(CartModel).where(
            CartModel.user_id == current_user.id,
            CartModel.product_id == product_id
        )
    )
    cart_item = query.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in your cart"
        )
        
    await session.delete(cart_item)
    await session.commit()

    cache_key = get_cart_cache_key(current_user.id)
    await redis.delete(cache_key)

@cart_router.patch("/{product_id}", response_model=CartResponseSchema)
async def update_cart_item_quantity(
    product_id: int,
    data: CartUpdateSchema,
    session: SessionDep, 
    current_user: CurrentUserDep,
    redis: Redis = Depends(get_redis)
):
    query = await session.execute(
        select(CartModel).where(
            CartModel.user_id == current_user.id,
            CartModel.product_id == product_id
        )
    )
    cart_item = query.scalar_one_or_none()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in your cart"
        )

    cart_item.quantity = data.quantity

    await session.commit()

    cache_key = get_cart_cache_key(current_user.id)
    await redis.delete(cache_key)

    result = await session.execute(
        select(CartModel)
        .options(joinedload(CartModel.products))
        .where(CartModel.id == cart_item.id)
    )
    
    return result.scalar_one()