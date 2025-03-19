from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Column
from sqlalchemy import String
from datetime import datetime
from typing import Optional

# ✅ Définition de la classe de base pour la conversion ORM → Pydantic
class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True  # Permet de convertir un modèle ORM en Pydantic

# ✅ Modèle de base pour une agence
class AgenceBase(OurBaseModel):
    nom_agence: str
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    adresse: str
    telepon: str  # 🔹 Ajout du champ téléphone pour éviter les erreurs de NULL

# ✅ Modèle pour l'inscription d'une agence (inclut les champs sensibles)
class AgenceRegister(AgenceBase):
    password: str
    confirm_password: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")  # 🔹 Suppression de `unique=True`

# ✅ Modèle pour la sortie de données (ex. réponse API)
class AgenceOut(AgenceBase):
    id: int
    
