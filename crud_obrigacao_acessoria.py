from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import models, schemas

def create_obrigacao_acessoria(database: Session, obrigacao_acessoria: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao_acessoria.model_dump())
    try:
        database.add(db_obrigacao)
        database.commit()
        database.refresh(db_obrigacao)
        return db_obrigacao
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao adicionar a obrigação acessória ao banco de dados.")

def get_obrigacao_acessoria_by_id(database: Session, obrigacao_id: int):
    return database.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()

def get_obrigacao_acessoria_all(database: Session):
    return database.query(models.ObrigacaoAcessoria).all()

def delete_obrigacao_acessoria(database: Session, obrigacao_id: int):
    db_obrigacao = database.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    try:
        database.delete(db_obrigacao)
        database.commit()
        return db_obrigacao
    except IntegrityError as e:
        database.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao remover a obrigação acessória.")

def update_obrigacao_acessoria(database: Session, obrigacao_id: int, obrigacao_update: schemas.ObrigacaoAcessoriaUpdate):
    db_obrigacao = database.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()

    if not db_obrigacao:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada.")
    
    db_obrigacao.nome = obrigacao_update.nome
    db_obrigacao.periodicidade = obrigacao_update.periodicidade

    try:
        database.commit()
        database.refresh(db_obrigacao)
        return db_obrigacao
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Houve um erro ao atualizar a obrigação acessória no banco de dados.")
