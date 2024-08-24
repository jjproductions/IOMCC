from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://'+os.getenv("DB_IOM_USER")+':'+os.getenv("DB_IOM_PASSWORD")+'@'+os.getenv("DB_SERVER")+"/"+os.getenv("DB_IOM_DATABASE")
SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.DB_IOM_USER}:{settings.db_iom_password}@{settings.DB_SERVER}/{settings.DB_IOM_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()