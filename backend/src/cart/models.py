from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, ForeignKey
import datetime

class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CartModel(user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})>"