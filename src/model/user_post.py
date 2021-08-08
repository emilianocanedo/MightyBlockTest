from datetime import datetime
from flask_restx.fields import DateTime

from sqlalchemy import Column, Integer, LargeBinary, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from model.base import Base, UpdateMixin


class UserPost(UpdateMixin, Base):
    __tablename__ = 'userpost'
    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String(280), nullable=True)
    image = Column(LargeBinary, nullable=True)
    likes = Column(Integer, default=0)
    created_dt = Column(DateTime, nullable=False, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
