from typing import List, Optional
from sqlmodel import Field, SQLModel
import sqlalchemy as sa
from datetime import datetime

from app.models.enums.moteur import Moteur
from app.models.enums.transmission import Transmission

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marque: str
    moteur: Moteur = Field(default=Moteur.Essence)
    annee: int  # L'année de fabrication
    prixParJour: int
    disponibilité: bool = Field(default=True)
    agence_id: int = Field(foreign_key="agence.id")
    transmission: Transmission = Field(default=Transmission.Manuelle)
    climatisation: bool = Field(default=True)
    kilometrage: int
    photo: List[str] = Field(default_factory=list, sa_column=sa.Column(sa.JSON))
    description: Optional[str] = Field(default=None, nullable=True)
    garantie: int
    created_at: datetime = Field(default_factory=datetime.now)
