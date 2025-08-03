from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
import os

# Database configuration
DATABASE_URL = config(
    'DATABASE_URL', 
    default='sqlite:///./old_age_home.db'
)

# For SQLite, we need to add check_same_thread=False
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database dependency
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
