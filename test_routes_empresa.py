import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Certifique-se de que 'main' é o nome do arquivo onde você configurou o FastAPI app
from db import Base  # Importe get_db aqui
from models import Empresa
from routes_empresa import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_get_empresa_all(client, db):
    # Adicionando uma empresa para testar a listagem
    empresa = Empresa(
        nome="Empresa Teste 2",
        endereco="Rua Teste, 456",
        email="teste2@example.com",
        telefone="987654321",
        cnpj="45678901234567"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    response = client.get("/empresa/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["nome"] == "Empresa Teste 2"

def test_create_empresa(client):
    response = client.post(
        "/empresa/",
        json={
            "nome": "Empresa Teste",
            "endereco": "Rua Teste, 123",
            "email": "teste@example.com",
            "telefone": "123456789",
            "cnpj": "12345678901234"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert data["email"] == "teste@example.com"
    assert data["cnpj"] == "12345678901234"

def test_get_empresa_by_id(client, db):
    # Adicionando uma empresa para testar a busca por ID
    empresa = Empresa(
        nome="Empresa Teste 3",
        endereco="Rua Teste, 789",
        email="teste3@example.com",
        telefone="123987456",
        cnpj="78901234567890"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    response = client.get(f"/empresa/{empresa.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste 3"
    assert data["email"] == "teste3@example.com"

def test_delete_empresa(client, db):
    # Adicionando uma empresa para testar a exclusão
    empresa = Empresa(
        nome="Empresa Teste 4",
        endereco="Rua Teste, 1011",
        email="teste4@example.com",
        telefone="1234567890",
        cnpj="10111213141516"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    response = client.delete(f"/empresa/{empresa.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste 4"

    # Verificando se a empresa foi realmente excluída
    response = client.get(f"/empresa/{empresa.id}/")
    assert response.status_code == 404

def test_update_empresa(client, db):
    # Adicionando uma empresa para testar a atualização
    empresa = Empresa(
        nome="Empresa Teste 5",
        endereco="Rua Teste, 1213",
        email="teste5@example.com",
        telefone="1234567890",
        cnpj="12131415161718"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    response = client.put(
        f"/empresa/{empresa.id}",
        json={
            "nome": "Empresa Teste Atualizada",
            "endereco": "Rua Teste Atualizada, 123",
            "email": "atualizado@example.com",
            "telefone": "0987654321",
            "cnpj": "18171615141312"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste Atualizada"
    assert data["email"] == "atualizado@example.com"
    assert data["cnpj"] == "18171615141312"
