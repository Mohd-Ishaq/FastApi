from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Integer, String
from .database import Base
from sqlalchemy import Column
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class app(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("post", back_populates="user")


class post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    url_type = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    user = relationship("app", back_populates="posts")
