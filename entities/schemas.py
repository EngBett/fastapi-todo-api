from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel


class RegisterModel(BaseModel):
    id: Optional[UUID] = uuid4()
    email: str
    full_name: str
    active: Optional[bool]
    password: str

    class Config:
        orm_mode = True


class LoginModel(BaseModel):
    email: str
    password: str


class TaskModel(BaseModel):
    id: Optional[UUID] = uuid4()
    title: str
    description: str
    complete: Optional[bool] = False
    user_id: Optional[UUID]

    class Config:
        orm_mode = True
