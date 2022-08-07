from sqlalchemy import Column, Integer, String, types

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    cookie = Column(types.JSON, nullable=True)
    freelancer_id = Column(Integer, nullable=True)
