from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from typing import List, Optional
from app import db

class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select"
    )

    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    # ОСЬ ЦЕ ПОЛЕ, ЯКЕ МИ ДОДАЄМО:
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=expression.true())

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'), nullable=True)
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")

    def __repr__(self) -> str:
        return f"<Product {self.name} - ${self.price}>"