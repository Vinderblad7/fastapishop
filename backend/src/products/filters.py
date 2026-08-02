from sqlalchemy import or_, select
from src.products.models import ProductModel
from src.products.schemas import ProductFilterSchema, PaginationSchema

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

def get_filter_cache_key(filters: ProductFilterSchema, pagination: PaginationSchema) -> str:
    filter_dict = filters.model_dump(exclude_unset=True)
    pagination_dict = pagination.model_dump()
    combined_dict = {**filter_dict, **pagination_dict}
    parts = [f"{k}={v}" for k, v in sorted(combined_dict.items())]
    return f"products:cache:{':'.join(parts)}"  