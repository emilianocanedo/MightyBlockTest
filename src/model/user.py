import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base, UpdateMixin


class User(UpdateMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)
    # M:1
    posts = relationship("UserPost", backref="user")
