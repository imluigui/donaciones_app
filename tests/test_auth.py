import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
from app.auth import get_password_hash

# Configuración de base de datos para pruebas
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)
    client = TestClient(app)
    yield client
    SQLModel.metadata.drop_all(engine)

def test_register_user(client):
    response = client.post(
        "/register/",
        json={"email": "test@example.com", "nombre": "Test User", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario registrado exitosamente"

def test_login_user(client):
    # Registrar usuario
    client.post(
        "/register/",
        json={"email": "login@example.com", "nombre": "Test User", "password": "password123"}
    )

    # Intentar login
    response = client.post(
        "/login/",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
