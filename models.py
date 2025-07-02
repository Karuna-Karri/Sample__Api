from sqlalchemy import Column, Integer, String
from database import Base

class Developer(Base):
    __tablename__ = "developers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    skills = Column(String(100))
    experience_years = Column(Integer)
    phone_number = Column(Integer, unique=True)
