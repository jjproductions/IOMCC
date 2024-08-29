from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from .db import Base


class Type_DB(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Role_DB(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class UserAuth_DB(Base):
    __tablename__ = "usersAuth"
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    password = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)

class Users_DB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text('now()'))
    name  = Column(String, nullable=False)
    card_id = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=True, server_default="true")
    comments = Column(String, nullable=True)
