# Import necessary modules from SQLAlchemy and project-specific modules.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
import pytest
from app.core.database import Base
from alembic import command


#TEST DATABASE
SQLALCHEMY_TEST_DATABASE_URL = f'mysql+pymysql://{settings.test_database_username}:{settings.test_database_password}@{settings.test_database_hostname}:{settings.test_database_port}/{settings.test_database_name}'

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, pool_size=12, max_overflow=16)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



