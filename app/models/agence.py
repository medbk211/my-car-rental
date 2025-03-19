from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from app.models.enums.agenceStatus import AgenceStatus



class Agence(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nom_agence: str = Field(index=True, nullable=False)
    email: Optional[str] = Field(default=None, index=True)
    téléphone: str = Field(default=None, nullable=False)
    adresse: str = Field(default=None, nullable=False)
    status: AgenceStatus = Field(default=AgenceStatus.INACTIVE)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)

    
