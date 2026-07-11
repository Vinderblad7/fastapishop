from fastapi import APIRouter, HTTPException, status 
from sqlalchemy import select
from slugify import slugify
from src.dependencies import SessionDep

from src.categories.schemas import CategoryCreateSchema, CategoryResponseSchema, CategoryUpdateSchema
from src.categories.models import CategoryModel

categories_router = APIRouter(prefix="/categories", tags=["Categories"])

@categories_router.post("", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_category(data: CategoryCreateSchema, session: SessionDep):
    category_slug = slugify(data.name)

    category = CategoryModel(
        name = data.name,
        slug = category_slug
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

@categories_router.get("", response_model=list[CategoryResponseSchema])
async def get_all(session: SessionDep):
    query = await session.execute(select(CategoryModel))
    categories = query.scalars().all()
    return categories

@categories_router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_by_id(category_id: int, session: SessionDep):
    query = await session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
    category = query.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found")
    return category

@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(category_id: int, session: SessionDep):
    query = await session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
    category = query.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found")
    await session.delete(category)
    await session.commit()

@categories_router.patch("/{category_id}", response_model=CategoryResponseSchema)
async def patch_by_id(category_id: int, data: CategoryUpdateSchema, session: SessionDep):
    query = await session.execute(select(CategoryModel).where(CategoryModel.id == category_id))
    category = query.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = data.model_dump(exclude_unset=True)
    
    if "name" in update_data:
        update_data["slug"] = slugify(update_data["name"])
    
    for key, value in update_data.items():
        setattr(category, key, value)
        
    session.add(category)
    await session.commit()
    await session.refresh(category)
    
    return category