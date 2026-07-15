from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime
from src.products.schemas import ProductResponseSchema

class OrderCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="Your email")
    phone_number: PhoneNumber = Field(..., description="Your phone number")
    address: str = Field(..., max_length=100, description="Your address")


class OrderItemResponseSchema(BaseModel):
    product: ProductResponseSchema
    quantity: int
    price_at_purchase: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponseSchema(BaseModel):
    id: int
    status: str
    total_price: int
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponseSchema]

    model_config = ConfigDict(from_attributes=True)