from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ProductBaseSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description="Product name")
    description: str = Field(..., min_length=3, max_length=1000,
                             description="Product description")
    price: float = Field(..., gt=0,
                         description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: str = Field(..., description="URL or path to the product image")

class ProductCreateSchema(ProductBaseSchema):
    pass

class ProductResponseSchema(ProductBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150, description="New product name")
    description: str | None = Field(None, max_length=1000, description="New product description")
    price: float | None = Field(None, gt=0, description="New price")
    category_id: int | None = Field(None, description="New category ID")
    image_url: str | None = Field(None, description="New URL or path to the product image")

class ProductFilterSchema(BaseModel):
    search: str | None = Field(None, description="Search by name or description")
    min_price: float | None = Field(None, description="Min price")
    max_price: float | None = Field(None, description="Max price")
    category_id: int | None = Field(None, description="Category ID")