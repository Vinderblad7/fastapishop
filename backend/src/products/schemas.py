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
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)