import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi.testclient import TestClient
from app.main import app
import pytest
from fastapi import status
from app.core.schemas import UserCreate
from app.core import crud

client = TestClient(app)

@pytest.mark.asyncio
async def test_register(client):
    user = {
        "USER_ID": "testuser",
        "PSSWRD": "testpassword",
        "USER_NM": "testname",
        "EMAIL": "testuser@example.com",
        "PHONE_NO": 1234567890
    }

    response = await client.post("/register", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["EMAIL"] == user["EMAIL"]
    assert "USER_MNG_ID" in data

@pytest.mark.asyncio
async def test_register_existing_email(client, db):
    # First registration
    user = UserCreate(
        USER_ID="testuser1",
        PSSWRD="testpassword",
        USER_NM="testname1",
        EMAIL="testuser1@example.com",
        PHONE_NO=1234567890
    )
    await crud.user_create(db, user)

    # Try to register with the same email
    new_user = {
        "USER_ID": "testuser2",
        "PSSWRD": "testpassword",
        "USER_NM": "testname2",
        "EMAIL": "testuser1@example.com",
        "PHONE_NO": 1234567891
    }

    response = await client.post("/register", json=new_user)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == f"Email {new_user['EMAIL']} is already registered"

@pytest.mark.asyncio
async def test_register_existing_username(client, db):
    # First registration
    user = UserCreate(
        USER_ID="testuser2",
        PSSWRD="testpassword",
        USER_NM="testname2",
        EMAIL="testuser2@example.com",
        PHONE_NO=1234567891
    )
    await crud.user_create(db, user)

    # Try to register with the same username
    new_user = {
        "USER_ID": "testuser3",
        "PSSWRD": "testpassword",
        "USER_NM": "testname2",
        "EMAIL": "testuser3@example.com",
        "PHONE_NO": 1234567892
    }

    response = await client.post("/register", json=new_user)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == f"Username {new_user['USER_NM']} is already taken"  





