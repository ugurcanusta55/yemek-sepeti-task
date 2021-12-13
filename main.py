from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
import publisher

from init_data import create_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/restaurants", response_model=List[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    restaurants = crud.get_restaurants(db, skip=skip, limit=limit)
    return restaurants


@app.get("/food-categories", response_model=List[schemas.FoodCategory])
def read_food_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/foods", response_model=List[schemas.Food])
def read_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    foods = crud.get_foods(db, skip=skip, limit=limit)
    return foods


@app.get("/order/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("skip", skip)
    orders = crud.get_orders(db, skip=skip, limit=limit)
    print("orders", orders)
    return orders


@app.post("/order/", response_model=schemas.SuccessResponse)
def create_order(order: schemas.CreateOrder):
    publisher.create_order(order)
    return {"status": True}

@app.put("/order/", response_model=schemas.SuccessResponse)
def confirm_order(order_id: int):
    publisher.confirm_orders({"order_id": order_id})
    return {"status": True}