from sqlalchemy import Boolean, DateTime, Text, Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy_utils import URLType
from slugify import slugify
from datetime import datetime

from database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String, unique=True)

    products = relationship("Product", back_populates="categories")

    def __init__(self, *args, **kwargs):
        if not "slug" in kwargs:
            kwargs["slug"] = slugify(kwargs.get("name", ""))
        super(Category, self).__init__(*args, **kwargs)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(Text)
    url = Column(URLType)
    price = Column(Integer)
    inStock = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    slug = Column(String, unique=True)

    category_id = Column(Integer, ForeignKey("category.id"))
    categories = relationship("Category", back_populates="products")

    def __init__(self, *args, **kwargs):
        if not "slug" in kwargs:
            kwargs["slug"] = slugify(kwargs.get("name", ""))
        super(Product, self).__init__(*args, **kwargs)
