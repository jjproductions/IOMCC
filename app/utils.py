from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(pw: str):
    return pwd_context.hash(pw)

def verify(pw:str, hash_pw:str):
    
    return pwd_context.verify(pw,hash_pw)