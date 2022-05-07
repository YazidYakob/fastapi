from typing import List
from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from starlette import status
from .. import models, schema, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash Password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{uid}', response_model=schema.UserOut)
def get_user(uid: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.uid == uid).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {uid} is not found")

    return user
