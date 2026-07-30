from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, func
from src.dependencies import SessionDep
from src.products.schemas import ProductCreateSchema, ProductResponseSchema, ProductUpdateSchema, ProductFilterSchema, PaginatedProductsResponseSchema
from src.products.filters import apply_product_filters
from src.products.models import ProductModel
from src.products.schemas import PaginationSchema
from src.database import get_redis
from redis.asyncio import Redis
from src.products.filters import get_filter_cache_key
import json

products_router = APIRouter(prefix="/products", tags=["Products"])

@products_router.post("", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreateSchema, session: SessionDep):
    product = ProductModel(
        name = data.name,
        description = data.description,
        price = data.price,
        category_id = data.category_id,
        image_url = data.image_url
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

# @products_router.get("", response_model=list[ProductResponseSchema])
# async def get_all(session: SessionDep):
#     query = await session.execute(select(ProductModel))
#     products = query.scalars().all()
#     return products

@products_router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_by_id(product_id: int, session: SessionDep):
    query = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = query.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found")
    return product

@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, session: SessionDep):
    query = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = query.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found")
    await session.delete(product)
    await session.commit()

@products_router.patch("/{product_id}", response_model=ProductResponseSchema)
async def patch_by_id(product_id: int, data: ProductUpdateSchema, session: SessionDep):
    query = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = query.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(product, key, value)
        
    session.add(product)
    await session.commit()
    await session.refresh(product)
    
    return product

@products_router.get("", response_model=PaginatedProductsResponseSchema)
async def get_products(
    session: SessionDep,
    filters: ProductFilterSchema = Depends(),
    pagination: PaginationSchema = Depends(),
    redis: Redis = Depends(get_redis)
):
    cache_key = get_filter_cache_key(filters, pagination)

    cached_data = await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
        
    query = select(ProductModel)
    query = apply_product_filters(query, filters)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar_one()
    
    offset = (pagination.page - 1) * pagination.limit
    paginated_query = query.limit(pagination.limit).offset(offset)
    
    result = await session.execute(paginated_query)
    products = result.scalars().all()

    products_data = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
            "category_id": product.category_id,
            "image_url": product.image_url,
        }
        for product in products
    ]

    response_payload = {
        "items": products_data,
        "total": total,
        "page": pagination.page,
        "limit": pagination.limit
    }

    await redis.set(cache_key, json.dumps(response_payload), ex=60)

    return response_payload