import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Certifique-se de que 'main' é o nome do arquivo onde você configurou o FastAPI app
from db import Base  # Importe get_db aqui
from routes_obrigacao_acessoria import get_db
from models import ObrigacaoAcessoria, Empresa
from crud_empresa import get_empresa_by_cnpj  # Importe get_empresa_by_cnpj aqui

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")  # Altere para "function"
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")  # Altere para "function"
def client(db):  # client depende de db, então o escopo precisa ser igual ou menor
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_get_obrigacao_acessoria_all(client, db):
    # Adicionando uma obrigação acessória para testar a listagem
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

    obrigacao = ObrigacaoAcessoria(
        nome="Obrigação Teste 2",
        periodicidade="anual",
        empresa_id=empresa.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)

    response = client.get("/obrigacao_acessoria/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["nome"] == "Obrigação Teste 2"

def test_get_obrigacao_acessoria_by_id(client, db):
    # Adicionando uma obrigação acessória para testar a busca por ID
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

    obrigacao = ObrigacaoAcessoria(
        nome="Obrigação Teste 3",
        periodicidade="trimestral",
        empresa_id=empresa.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)

    response = client.get(f"/obrigacao_acessoria/{obrigacao.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Obrigação Teste 3"
    assert data["periodicidade"] == "trimestral"

def test_delete_obrigacao_acessoria(client, db):
    # Adicionando uma obrigação acessória para testar a exclusão
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

    obrigacao = ObrigacaoAcessoria(
        nome="Obrigação Teste 4",
        periodicidade="mensal",
        empresa_id=empresa.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)

    response = client.delete(f"/obrigacao_acessoria/{obrigacao.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Obrigação Teste 4"

    # Verificando se a obrigação acessória foi realmente excluída
    response = client.get(f"/obrigacao_acessoria/{obrigacao.id}")
    assert response.status_code == 404

def test_update_obrigacao_acessoria(client, db):
    # Adicionando uma obrigação acessória para testar a atualização
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

    obrigacao = ObrigacaoAcessoria(
        nome="Obrigação Teste 5",
        periodicidade="anual",
        empresa_id=empresa.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)

    response = client.put(
        f"/obrigacao_acessoria/{obrigacao.id}",
        json={
            "nome": "Obrigação Teste Atualizada",
            "periodicidade": "trimestral"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Obrigação Teste Atualizada"
    assert data["periodicidade"] == "trimestral"
