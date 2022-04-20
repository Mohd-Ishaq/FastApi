from fastapi import FastAPI, HTTPException, status
from . import models
from .database import engine, get_db
from .router import user
from .router import post, auth
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
