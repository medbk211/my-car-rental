import logging
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.user import User
from app.models.agence import Agence
from app.schemas.user import UserCreate
from app.schemas.agence import AgenceRegister

logger = logging.getLogger(__name__)

# Configuration de passlib pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_all_users(db: AsyncSession):
    """Récupère tous les utilisateurs."""
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user_id(db: AsyncSession, id: int):
    """Récupère un utilisateur par son ID."""
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def get_user_email(db: AsyncSession, email: str):
    """Récupère un utilisateur par son email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

def hash_password(password: str) -> str:
    """Hache un mot de passe en utilisant bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe en clair correspond au mot de passe haché."""
    return pwd_context.verify(plain_password, hashed_password)

async def add_user(db: AsyncSession, user_data: UserCreate) -> JSONResponse:
    """
    Ajoute un nouvel utilisateur dans la base de données.
    Retourne une réponse JSON avec un message et l'ID de l'utilisateur créé.
    """
    # Vérifier si l'email est déjà utilisé
    existing_user = await get_user_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    try:
        # Préparation des données utilisateur en excluant le champ 'confirm_password'
        user_dict = user_data.model_dump(exclude={'confirm_password'})
        
        # Hacher le mot de passe
        if user_data.password:
            user_dict["password"] = hash_password(user_data.password)
        
        # Création d'un nouvel utilisateur avec le rôle "USER" et activation immédiate
        new_user = User(**user_dict, role="USER", is_active=True)
        db.add(new_user)
        await db.flush()          # Permet d'obtenir l'ID sans commit
        await db.commit()
        await db.refresh(new_user) # Recharge l'objet après commit
        
        return JSONResponse(
            status_code=201,
            content={"message": "Utilisateur ajouté avec succès", "user_id": new_user.id}
        )
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Erreur lors de l'ajout de l'utilisateur : {e}")
        raise HTTPException(status_code=500, detail="Erreur de base de données")

async def register_agency(db: AsyncSession, agency_data: AgenceRegister) -> JSONResponse:
    """
    Inscrit une nouvelle agence dans la base de données.
    Retourne une réponse JSON indiquant que l'agence a été enregistrée et est en attente d'approbation.
    """
    existing_user = await get_user_email(db, email=agency_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    if agency_data.password != agency_data.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")
    
    try:
        hashed_password = hash_password(agency_data.password)
        
        # Création d'un nouvel utilisateur avec le rôle "AGENCE" et inactif par défaut
        new_user = User(
            email=agency_data.email,
            password=hashed_password,
            role="AGENCE",
            is_active=False,
            téléphone=agency_data.telepon
        )
        db.add(new_user)
        await db.flush()  # Permet d'obtenir l'ID sans commit
        
        # Création de la nouvelle agence associée à l'utilisateur
        new_agency = Agence(
            nom_agence=agency_data.nom_agence,
            adresse=agency_data.adresse,
            téléphone=agency_data.telepon,
            email=agency_data.email,
            user_id=new_user.id
        )
        db.add(new_agency)
        await db.commit()
        
        return JSONResponse(
            status_code=201,
            content={"message": "Agence enregistrée avec succès. En attente d'approbation par l'administrateur."}
        )
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Erreur lors de l'enregistrement de l'agence : {e}")
        raise HTTPException(status_code=500, detail="Une erreur est survenue lors de l'enregistrement de l'agence.")
