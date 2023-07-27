from typing import Optional
from pydantic import BaseModel, EmailStr

# from models.event import fix_date
# pydantic schema for Event CRUD


class EventBase(BaseModel):
    event_name: str
    description: str
    venue: str


# creating a new Event
class EventCreate(EventBase):
    pass


# Reading new events


class EventRead(BaseModel):
    id: int
    event_name: str
    description: str
    venue: str
    


    class Config:
        orm_mode = True

class EventUpdate(BaseModel):
    id: int
    event_name:str
    description: str
    venue: str


    class Config:
        orm_mode = True


class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass

class UserGrab(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserRead(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    id:int | None
    firstName: str | None
    lastName: str | None
    password: str | None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
