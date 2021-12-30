from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database import get_db


from app.models import app
from app.utils import AuthRequest
from app.oauth2 import gen

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def logn(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(app).filter(app.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    v = AuthRequest(request.password, user.password)
    if not v:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = gen({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
