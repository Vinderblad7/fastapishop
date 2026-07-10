from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    products: Mapped[list["ProductModel"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"