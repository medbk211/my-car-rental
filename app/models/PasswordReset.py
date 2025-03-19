from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column
import sqlalchemy as sa

class PasswordReset(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    utilisateur_id: int = Field(foreign_key="user.id")
    token: str
    date_creation: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(sa.DateTime(timezone=True))
    )
    date_expiration: datetime = Field(
        sa_column=Column(sa.DateTime(timezone=True))
    )
    is_used: bool = Field(default=False)

  