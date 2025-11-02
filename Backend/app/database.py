from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/dermfridge_db")

# Connect engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Create a session
SessionLocal = sessionmaker(bind=engine)

# Define an Item model
class Item(Base):
    __tablename__ = "fridge"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    added_date = Column(DateTime, default=datetime.utcnow)
