from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from src.dependencies import SessionDep
from src.products.schemas import ProductCreateSchema, ProductResponseSchema, ProductUpdateSchema, ProductFilterSchema
from src.products.filters import apply_product_filters
from src.products.models import ProductModel
from src.products.schemas import PaginationSchema

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

@products_router.get("", response_model=list[ProductResponseSchema])
async def get_products(
    session: SessionDep,
    filters: ProductFilterSchema = Depends(),
    pagination: PaginationSchema = Depends()
):
    query = select(ProductModel)
    
    query = apply_product_filters(query, filters)
    
    offset = (pagination.page - 1) * pagination.limit
    
    query = query.limit(pagination.limit).offset(offset)
    
    result = await session.execute(query)
    products = result.scalars().all()
    
    return products