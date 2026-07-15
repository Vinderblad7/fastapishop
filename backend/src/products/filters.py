from sqlalchemy import or_, select
from src.products.models import ProductModel
from src.products.schemas import ProductFilterSchema

def apply_product_filters(query, filters: ProductFilterSchema):
    if filters.search:
        query = query.where(
            or_(
                ProductModel.name.ilike(f"%{filters.search}%"),
                ProductModel.description.ilike(f"%{filters.search}%")
            )
        )
        
    if filters.min_price is not None:
        query = query.where(ProductModel.price >= filters.min_price)
        
    if filters.max_price is not None:
        query = query.where(ProductModel.price <= filters.max_price)
        
    if filters.category_id is not None:
        query = query.where(ProductModel.category_id == filters.category_id)
        
    return query