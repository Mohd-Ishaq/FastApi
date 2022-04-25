from fastapi import APIRouter, HTTPException, status
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Depends, File
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.oauth2 import get_current
from app.schemas import post1, resp
from app.models import post
from typing import List
import shutil

router = APIRouter(prefix="/post", tags=["Posts"])


@router.post("/")
def creat(
    request: post1, db: Session = Depends(get_db), current_user=Depends(get_current)
):
    crete_post = post(user_id=current_user.id, **request.dict())
    db.add(crete_post)
    db.commit()
    db.refresh(crete_post)
    return crete_post


@router.get("/all", response_model=List[resp])
def get_all(db: Session = Depends(get_db), current_user=Depends(get_current)):
    get_post = db.query(post).all()
    return get_post


@router.get("/one/{id}")
def get1(id: int, db: Session = Depends(get_db), current_user=Depends(get_current)):
    get1_post = db.query(post).filter(post.id == id)
    get_o = get1_post.first()
    return get_o


@router.put("/{id}", response_model=resp)
def post_upt(
    id: int,
    request: post1,
    db: Session = Depends(get_db),
    current_user=Depends(get_current),
):
    update_post = db.query(post).filter(post.id == id)
    updated = update_post.first()
    if not updated:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
    update_post.update(request.dict(), synchronize_session=False)
    db.commit()
    return updated


@router.delete("/delete/{id}")
def delet(id: int, db: Session = Depends(get_db), current_user=Depends(get_current)):
    delete = db.query(post).filter(post.id == id)
    delete_user = delete.first()
    if not delete_user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"this id:{id} does not exist"
        )
    delete.delete()
    db.commit()
    return delete_user


@router.post("/image")
def Upload_Image(image: UploadFile = File(...), current_user=Depends(get_current)):
    filename = image.filename
    path = f"static//{filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        buffer.close()
    return path
