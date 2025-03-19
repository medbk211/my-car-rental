from typing import Optional
from sqlmodel import Field, SQLModel
import sqlalchemy as sa



class Avis(SQLModel, table=True):
    id:int= Field(default=None, primary_key=True)
    note: int = Field(sa_column=sa.Column(sa.Integer, sa.CheckConstraint("note BETWEEN 1 AND 5")))
    commentaire: Optional[str] = Field(default=None, nullable=True)
    utilisateur_id: int = Field(foreign_key="user.id")
    car_id: int = Field(foreign_key="car.id")


