from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from src.products.schemas import ProductResponseSchema

class CartAddSchema(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., description="Product quantity")

class CartResponseSchema(BaseModel):
    id: int
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., description="Product quantity")
    products: ProductResponseSchema
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CartUpdateSchema(BaseModel):
    quantity: int = Field(..., ge=1, description="New quantity")