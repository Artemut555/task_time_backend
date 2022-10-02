from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from datetime import datetime


class Recipe(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(256), nullable=False)
    url = Column(String(256), index=True, nullable=True)
    source = Column(String(256), nullable=True)
    start_time = Column(DateTime, default=datetime.now())
    finish_time = Column(DateTime, default=datetime.now())
    task_finished = Column(Integer)
    submitter_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    submitter = relationship("User", back_populates="recipes")

