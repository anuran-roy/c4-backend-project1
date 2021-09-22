from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker   

DB_PATH = 'sqlite:///./blogs.sqlite3'

engine = create_engine(DB_PATH, connect_args = {"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()