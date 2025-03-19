from sqlalchemy import Column, DateTime, func

from sqlmodel import Field, SQLModel, Column
from datetime import datetime, date

class AdminAudit(SQLModel, table=True):

    id: int  = Field(default=None, primary_key=True)
    admin_id: int = Field(nullable=False)
    action: str  = Field(nullable=False)
    target_id: int = Field(nullable=False)
    timestamp: datetime = Field(sa_column=Column(DateTime, nullable=False, server_default=func.now()))


