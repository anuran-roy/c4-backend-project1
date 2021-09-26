from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from database import Base

class Blog(Base):

    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
