# Import necessary modules from SQLAlchemy and project-specific modules.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os


# PROD DATABASE 
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOSTNAME')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)
# Create the database engine using the URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=12, max_overflow=16)

# Create a session maker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for the models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    
    db = SessionLocal()
    try:
        # Yield the session to be used by the caller
        yield db
    finally:
        # Close the session when done
        db.close()



