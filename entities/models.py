from uuid import uuid4
from sqlalchemy import (Column, DateTime, ForeignKey, String, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship("Task", back_populates="user")

    def __repr__(self) -> str:
        return f"User {self.id} {self.full_name}"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    complete = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.id} {self.title}>"
