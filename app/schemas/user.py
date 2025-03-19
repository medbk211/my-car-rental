from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Column
from sqlalchemy import String
from datetime import date
from typing import Optional
from datetime import datetime


class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class UserBase(OurBaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    téléphone: str = Field(index=True)
    birth_date: Optional[date] = None

class UserCreate(UserBase):
    password: str = Field(index=True)
    confirm_password: str  # Ce champ est seulement pour la validation, il n'est pas enregistré dans la base

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None
class UserUpdate(UserBase):
    first_name: str
    last_name: str
    birth_date: date
    



class UserInDB(BaseModel):
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    password: str = Field(index=True)
