from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from src.dependencies import SessionDep, CurrentUserDep
from src.orders.schemas import OrderCreateSchema, OrderResponseSchema
from src.orders.models import OrderModel, OrderStatus, OrderItem
from src.cart.models import CartModel

orders_router = APIRouter(prefix="/orders", tags=["Orders"])

@orders_router.post("", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreateSchema, session: SessionDep, current_user: CurrentUserDep):
    query = await session.execute(
        select(CartModel).where(CartModel.user_id == current_user.id)
    )
    cart = query.scalars().all()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty"
        )

    total_sum = 0
    for item in cart:
        item_price = item.quantity * item.products.price  
        total_sum += item_price

    new_order = OrderModel(
        user_id=current_user.id,
        status=OrderStatus.PENDING,
        total_price=total_sum,
        email=data.email,
        phone_number=str(data.phone_number),
        address=data.address
    )
    session.add(new_order)
    await session.flush()

    for item in cart:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.products.price
        )
        session.add(order_item)

    await session.execute(
        delete(CartModel).where(CartModel.user_id == current_user.id)
    )

    await session.commit()
    
    await session.refresh(new_order)
    
    return new_order

@orders_router.get("", response_model=list[OrderResponseSchema])
async def get_orders_history(session: SessionDep, current_user: CurrentUserDep):
    query = await session.execute(
        select(OrderModel)
        .where(OrderModel.user_id == current_user.id)
        .options(
            selectinload(OrderModel.items).selectinload(OrderItem.product)
        )
    )
    orders = query.scalars().all()
    return orders

@orders_router.get("/{order_id}", response_model=OrderResponseSchema)
async def get_order_by_id(order_id: int, session: SessionDep, current_user: CurrentUserDep):
    query = await session.execute(
        select(OrderModel)
        .where(OrderModel.id == order_id)
        .options(
            selectinload(OrderModel.items).selectinload(OrderItem.product)
        )
    )
    order = query.scalar_or_none()

    if not order or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order

@orders_router.patch("/{order_id}/cancel", response_model=OrderResponseSchema)
async def cancel_order(order_id: int, session: SessionDep, current_user: CurrentUserDep):
    query = await session.execute(
        select(OrderModel)
        .where(OrderModel.id == order_id)
        .options(
            selectinload(OrderModel.items).selectinload(OrderItem.product)
        )
    )
    order = query.scalar_or_none()

    if not order or order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order in status '{order.status.value}'"
        )

    order.status = OrderStatus.CANCELED
    await session.commit()
    await session.refresh(order)

    return order