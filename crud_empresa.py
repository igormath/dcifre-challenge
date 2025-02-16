from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import models, schemas

def create_empresa(database: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.model_dump())
    try:
        database.add(db_empresa)
        database.commit()
        database.refresh(db_empresa)
        return db_empresa
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao adicionar a empresa ao banco de dados.")

def get_empresa_all(database: Session):
    return database.query(models.Empresa).all()

def get_empresa_by_id(database: Session, empresa_id: int):
    return database.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

def get_empresa_by_cnpj(database: Session, empresa_cnpj: str):
    return database.query(models.Empresa).filter(models.Empresa.cnpj == empresa_cnpj).first()

def delete_empresa(database: Session, empresa_id: int):
    empresa = database.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada no banco de dados.")
    
    try:
        database.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.empresa_id == empresa_id).delete(synchronize_session=False)
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao remover as obrigações acessórias desta empresa.")

    try:
        database.delete(empresa)
        database.commit()
        return empresa
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao remover a empresa.")

def update_empresa(database: Session, empresa_id: int, empresa: schemas.EmpresaUpdate):
    db_empresa = database.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()

    db_empresa.nome = empresa.nome
    db_empresa.endereco = empresa.endereco
    db_empresa.email = empresa.email
    db_empresa.telefone = empresa.telefone

    if empresa.cnpj != db_empresa.cnpj:
        cnpj_exists = database.query(models.Empresa).filter(
                models.Empresa.cnpj == empresa.cnpj,
                models.Empresa.id != empresa_id
            ).first()
        if cnpj_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe uma empresa cadastrada com este CNPJ.")
    
    db_empresa.cnpj = empresa.cnpj

    try:
        database.commit()
        database.refresh(db_empresa)
        return db_empresa
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao atualizar a empresa no banco de dados.")
