from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .config import settings
from . import schemas, models
from .db import get_db
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



def create_access_token(sub: dict, expires_delta: timedelta | None = None):
    to_encode = sub.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.algorithm)
    return encoded_jwt
    
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.algorithm])
        print(f"verify token:payload: {payload}")
        email: str = payload.get("sub")
        print(f"verify token:email: {email}")
        if not email:
            raise credentials_exception
            
        token_data = schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
        
    return token_data

''' def verify_access_role(auth_data, role_exception, db: Session = Depends(get_db)):
    #try catch
    #email = verify_access_token
    role_id = auth_data.get("role")
    email = auth_data.get("email")

    if not auth_data:
        raise role_exception
    else:
        print(f"{email} and {role_id}")
        role_results = db.query(models.Users_DB).join(
            models.Role_DB, models.Users_DB.role_id == models.Role_DB.id) #.filter(email==email)
        if not role_results:
            raise role_exception
        print(role_results)

    token_data = True
    
    
    return token_data   '''

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    print(f"get current user-token: {token}")
    return verify_access_token(token, credentials_exception)
    

""" def is_authorized(auth_data:str):  #role: int, email: str):
    role_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    return verify_access_role(auth_data, role_exception) """
