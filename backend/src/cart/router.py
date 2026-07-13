from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.dependencies import SessionDep, CurrentUserDep
from src.cart.models import CartModel  
from src.cart.schemas import CartAddSchema, CartResponseSchema, CartUpdateSchema

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

@cart_router.post("", response_model=CartResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    data: CartAddSchema, 
    session: SessionDep, 
    current_user: CurrentUserDep
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
    current_user: CurrentUserDep
):
    query = await session.execute(
        select(CartModel).where(CartModel.user_id == current_user.id)
    )
    cart_items = query.scalars().all()
    
    return cart_items

@cart_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, 
    session: SessionDep, 
    current_user: CurrentUserDep
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

@cart_router.patch("/{product_id}", response_model=CartResponseSchema)
async def update_cart_item_quantity(
    product_id: int,
    data: CartUpdateSchema,
    session: SessionDep, 
    current_user: CurrentUserDep
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
    await session.refresh(cart_item)
    
    return cart_item