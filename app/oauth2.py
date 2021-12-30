from datetime import date, datetime, timedelta
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from fastapi import status
from app.database import get_db
from app.models import app
from app.env_valid import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


ALGORITHM = setting.ALGORITHM
SECRET_KEY = setting.SECRET_KEY
EXPIRE_TIME = setting.EXPIRE_TIME


def gen(data: dict):
    a = data.copy()
    exp_time = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)
    a.update({"exp": exp_time})
    token = jwt.encode(a, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token, credential_exception):

    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = token_data.get("user_id")
        if id == None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return id


def get_current(token=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials",
        headers={"WWW-AUTHENTICATE": "BEARER"},
    )
    id = verify_token(token, credential_exception)
    user = db.query(app).filter(app.id == id).first()
    return user
