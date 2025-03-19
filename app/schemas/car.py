from datetime import datetime
from typing import Optional , List
from pydantic import BaseModel
from app.models.enums.moteur import Moteur
from app.models.enums.transmission import Transmission

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Permet de convertir depuis un objet SQLModel

class CarBase(OurBaseModel):
    marque: str
    moteur: Moteur# Vous pouvez utiliser le type Enum si souhaité
    annee: int
    prixParJour: int
    disponibilité: bool
    transmission:Transmission   # Vous pouvez utiliser le type Enum si souhaité
    climatisation: bool
    kilometrage: int
    description: Optional[str] = None
    garantie: int

class CarCreate(CarBase):
    # Le champ 'photo' est géré séparément via UploadFile, il n'est donc pas présent ici
    pass

class CarOut(CarBase):
    photo: List[str]
    id: int
    created_at: Optional[datetime] = None
