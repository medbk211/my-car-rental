from fastapi import UploadFile, HTTPException
from typing import List
import shutil
import os
import uuid
from app.models.enums.moteur import Moteur
from app.models.enums.transmission import Transmission


UPLOAD_DIR = "uploaded_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Liste des extensions d'images autorisées
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

def is_allowed_file(filename: str) -> bool:
    """Vérifie si le fichier a une extension autorisée."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_photos(files: List[UploadFile]) -> List[str]:
    file_paths = []
    for file in files:
        if not is_allowed_file(file.filename):
            raise HTTPException(status_code=400, detail=f"Le fichier {file.filename} n'est pas une image valide.")
        
        # Générer un nom unique pour chaque fichier
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Sauvegarder le fichier sur le disque
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement du fichier: {e}")
        
        file_paths.append(file_path)
    return file_paths
