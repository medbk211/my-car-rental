from sqlalchemy import Date
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import String
from pydantic import EmailStr
from sqlalchemy.sql import func
from datetime import datetime, date
from sqlalchemy import Column, DateTime
from app.models.enums.role import Role
from sqlalchemy.orm import Relationship
from typing import Optional





class User(SQLModel, table=True):
    id: int  = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column=Column("email", String, unique=True, nullable=False, index=True))
    password: str = Field(index=True ,nullable=False)
    role: Role = Field(nullable=False , default=Role.USER)
    is_active: bool = Field(default=True)

    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    birth_date: date = Field(nullable=True)


    téléphone: str = Field(index=True)
    created_at: datetime = Field(sa_column=Column(DateTime, nullable=False, server_default=func.now()))
    
    

    
