from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime



class Réservation(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    date_debut: datetime = Field(index=True)
    date_fin: datetime = Field(index=True)
    date_creation: datetime = Field(sa_column=Column("date_creation", type_=DateTime))  # Fixed this line
    date_annulation: Optional[datetime] = Field(default=None, nullable=True)  # Remove index=True
    utilisateur_id: int = Field(foreign_key="user.id", index=True)
    car_id: Optional[int] = Field(foreign_key="car.id", index=True, nullable=True)



