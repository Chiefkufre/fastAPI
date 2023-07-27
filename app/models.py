from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Boolean, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, TIME


from database import Base





class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    event_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    venue = Column(String, nullable=False)
    # date = Column(datetime)
    # time = Column(datetime)
    is_active = Column(Boolean, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()")
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="events")


class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    events = relationship("Event", back_populates="owner")

    def __str__(self):
        return f"{self.email}"