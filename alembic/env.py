from logging.config import fileConfig
from alembic import context
from sqlmodel import SQLModel
from app.database import engine_sync 
from dotenv import load_dotenv
import os
from app.models import ActivationCompte, agence, Avis, car, Paiement, PasswordReset, Réservation, user  , AdminAudit# Import des modèles
load_dotenv()
# Configuration d'Alembic
config = context.config




database_url = os.getenv("DATABASE_URL_SYNC")
url = config.get_main_option("sqlalchemy.url", database_url )
# Configuration des logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Définition de la metadata pour la migration
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Exécuter les migrations en mode hors ligne."""
   
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Exécuter les migrations en mode en ligne."""
    connectable = engine_sync  # Utilisation directe de l'engine défini dans database.py

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
