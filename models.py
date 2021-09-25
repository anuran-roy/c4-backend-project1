from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean
from database import Base

class Blog(Base):

    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
