from pydantic import BaseModel, Field, ConfigDict

class CategoryBaseSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description="Category name")

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryResponseSchema(CategoryBaseSchema):
    id: int
    slug: str = Field(..., min_length=3, max_length=100,
                      description="Slug")

    model_config = ConfigDict(from_attributes=True)