from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# URL de connexion à PostgreSQL
# DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:123456789@localhost/postgres"
# DATABASE_URL_SYNC = "postgresql://postgres:123456789@localhost/postgres"  # Suppression de "+asyncpg"

# Moteur asynchrone (utilisé par FastAPI)
engine_async = create_async_engine(settings.DATABASE_URL_ASYNC, echo=True)

# Moteur synchrone (utilisé par Alembic)
engine_sync = create_engine(settings.DATABASE_URL_SYNC, echo=True)

# Définition de la base de données
Base = declarative_base()

# Création d'une session asynchrone
AsyncSessionLocal = sessionmaker(
    bind=engine_async,
    class_=AsyncSession,
    expire_on_commit=False
)

# Création d'une session synchrone (pour Alembic)
SessionLocal = sessionmaker(bind=engine_sync)

# Fonction pour récupérer une session via un generator (utilisé avec Depends)
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
