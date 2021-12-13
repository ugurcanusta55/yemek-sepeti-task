from db import models
from sqlalchemy.orm import Session


def create_user(db: Session):
    db_user = models.User(email="ugurcanusta55@gmail.com", name="Ugurcan", surname="Usta")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
