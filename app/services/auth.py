from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models.user import User  
from app.database import get_session 
from app.core.config import settings
from app.api.crud.user import get_user_email
from app.services.storage import TOKEN_STORAGE




async def get_current_admin(
    db: Session = Depends(get_session)
) -> User:
    
    token = TOKEN_STORAGE.get("access_token") 
    try:
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=" token incorrect "
            )
        
       
        user: User = await get_user_email(db, user_email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="user not found"
            )
        
     
        
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="التوكن غير صحيح"
        )
