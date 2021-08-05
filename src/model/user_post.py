import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base, UpdateMixin


class UserPost(UpdateMixin, Base):
    __tablename__ = 'userpost'
    id = Column(Integer, primary_key=True, nullable=False)
    image_path = Column(String(50), nullable=True)
    likes = Column(Integer, nullable=True)
