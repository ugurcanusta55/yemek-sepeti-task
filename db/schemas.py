from typing import List, Optional

from pydantic import BaseModel

class SuccessResponse(BaseModel):
    status: bool


class Restaurant(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FoodCategory(BaseModel):
    id: int
    name: str
    restaurants: Restaurant

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    class Config:
        orm_mode = True


class Food(BaseModel):
    id: int
    name: str
    category: FoodCategory
    restaurant: Restaurant
    
    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    owner_id: int
    food: List[int]


class Order(BaseModel):
    id: int
    owner_id: int
    is_confirmed: bool
    food: List[Food]

    class Config:
        orm_mode = True