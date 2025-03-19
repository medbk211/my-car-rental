from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User

class ActivationCompte(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    date_creation: datetime = Field(default_factory=datetime.now, index=True)
    date_expiration: datetime = Field(index=True)
    utilisateur_id: int = Field(foreign_key="user.id")
    is_active: bool = Field(default=False, index=True)

