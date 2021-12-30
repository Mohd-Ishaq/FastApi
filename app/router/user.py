from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app import models
from app.database import engine, get_db
from app.schemas import UserBase, UserOut, updat
from typing import List
from app.utils import func
from app.oauth2 import get_current

router = APIRouter(tags=["Users"])


@router.get("/")
def hell():
    return "hello world!"


@router.post("/user", response_model=UserOut)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    hashed_password = func(request.password)
    created = models.app(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )
    db.add(created)
    db.commit()
    db.refresh(created)
    return created


@router.get("/user/all", response_model=List[UserOut])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.app).all()
    return user


@router.get("/user/{id}", response_model=UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
):
    user_query = db.query(models.app).filter(models.app.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )
    return user


@router.put("/user/{id}", response_model=UserOut)
def upd(
    id: int,
    request: updat,
    db: Session = Depends(get_db),
    current_user=Depends(get_current),
):
    update = db.query(models.app).filter(models.app.id == id)
    user_update = update.first()
    if not user_update:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
    update.update(request.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user_update)
    return user_update


@router.delete("/user/delete/{id}")
def delt(id: int, db: Session = Depends(get_db), current_user=Depends(get_current)):
    delete = db.query(models.app).filter(models.app.id == id)
    delete_user = delete.first()
    if not delete_user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
    delete.delete()
    db.commit()
    return delete_user
