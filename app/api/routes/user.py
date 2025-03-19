import logging
from datetime import datetime, timedelta
from typing import List
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.database import get_session as get_async_session
from app.models.user import User
from app.models.agence import Agence
from app.models.car import Car
from app.models.enums.role import Role
from app.models.enums.agenceStatus import AgenceStatus
from app.models.AdminAudit import AdminAudit
from app.schemas.user import UserCreate, UserOut, UserInDB
from app.schemas.agence import AgenceRegister, AgenceOut
from app.schemas.car import CarCreate, CarOut
from app.api.crud.user import get_user_email, add_user, register_agency, verify_password
from app.api.crud.car import save_photos
from app.services.auth import get_current_admin
from app.services.storage import TOKEN_STORAGE

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register-client", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_employee(user_data: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Crée un nouvel employé.
    """
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les mots de passe ne correspondent pas"
        )
    user = await add_user(db, user_data)
    return user


@router.post("/register-agency", response_model=AgenceOut, status_code=status.HTTP_201_CREATED)
async def register_agency_root(agency_data: AgenceRegister, db: AsyncSession = Depends(get_async_session)):
    """
    Crée une nouvelle agence.
    """
    if agency_data.password != agency_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Les mots de passe ne correspondent pas"
        )
    agency = await register_agency(db, agency_data)
    return agency


@router.put("/admin/activate/{agency_id}", status_code=status.HTTP_200_OK)
async def activate_agency_by_admin(
    agency_id: int,
    current_user: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Permet à un administrateur d'activer un compte d'agence.
    """
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé, privilèges d'administrateur requis"
        )

    result = await db.execute(select(Agence).filter(Agence.id == agency_id))
    agency = result.scalar_one_or_none()
    if not agency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agence introuvable"
        )
    if agency.status == AgenceStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'agence est déjà activée"
        )

    # Mise à jour du statut de l'agence
    agency.status = AgenceStatus.ACTIVE.value

    # Enregistrement de l'action dans le système d'audit
    audit_record = AdminAudit(
        admin_id=current_user.id,
        target_id=agency.id,
        action="ACTIVATION",
        timestamp=datetime.utcnow()
    )
    db.add(audit_record)

    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Erreur lors de l'activation de l'agence (ID {agency_id}) : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur lors de l'activation de l'agence"
        )

    await db.refresh(agency)
    return {"message": f"L'agence avec l'ID {agency_id} a été activée avec succès"}


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Génère un jeton d'accès JWT avec une durée d'expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: UserInDB, db: AsyncSession = Depends(get_async_session)):
    """
    Authentifie un utilisateur et génère un jeton d'accès JWT.
    """
    user: User = await get_user_email(db, email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )
   
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    TOKEN_STORAGE["access_token"] = access_token
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/agency/cars", response_model=CarOut, status_code=status.HTTP_201_CREATED)
async def add_car(
    car: str = Depends(CarCreate), 
    photos: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin),
):
    """
      Permet à un administrateur d'activer un compte d'agence.
    """
    if current_user.role != Role.AGENCE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé, privilèges d'administrateur requis"
        )
    
    result = await db.execute(select(Agence).filter(Agence.email == current_user.email))
    agency = result.scalar_one_or_none()

     
     
    """
    Ajoute une voiture pour une agence avec jusqu'à 3 photos.
    """
    if len(photos) > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 photos autorisées")
    
    try:
        # Enregistrer les photos et récupérer leurs chemins
        photo_paths = save_photos(photos)  # Vérifiez que cette fonction fonctionne correctement
        print(car)
        # Créer l'instance de la voiture en décompressant les données reçues et en ajoutant les photos
        car_data = Car(**car.dict(), photo=photo_paths, agence_id=agency.id )

        # Ajout à la base de données
        db.add(car_data)
        await db.flush()  # Permet d'obtenir l'ID généré avant le commit
        await db.commit()
        await db.refresh(car_data)  # Actualise l'objet avec les données en base

        return car_data

    except Exception as e:
        await db.rollback()  # Annule la transaction en cas d'erreur
        logger.error(f"Erreur lors de l'ajout de la voiture : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout de la voiture")
@router.get("/all_cars", response_model=List[CarOut], status_code=status.HTTP_200_OK)
async def get_all_cars(db: AsyncSession = Depends(get_async_session)):
    """
    Récupère toutes les voitures disponibles.
    """
    result = await db.execute(select(Car))
    cars = result.scalars().all()
    return cars