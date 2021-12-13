from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base


"""class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
"""

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="owner")


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    food_categories = relationship("FoodCategory", back_populates="restaurants")
    foods = relationship("Food", back_populates="restaurant")


class FoodCategory(Base):
    __tablename__ = "food_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    restaurants = relationship("Restaurant", back_populates="food_categories")
    foods = relationship("Food", back_populates="category")


association_table = Table('association', Base.metadata,
    Column('food_id', ForeignKey('foods.id'), primary_key=True),
    Column('order_id', ForeignKey('orders.id'), primary_key=True)
)


class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("food_categories.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    category = relationship("FoodCategory", back_populates="foods")
    restaurant = relationship("Restaurant", back_populates="foods")


class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    food = relationship("Food", secondary=association_table)
    is_confirmed = Column(Boolean, default=False)

    owner = relationship("User", back_populates="orders")