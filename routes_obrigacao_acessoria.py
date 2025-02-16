from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import crud_obrigacao_acessoria, crud_empresa,models, schemas
from db import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)
router_obrigacao_acessoria = APIRouter()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@router_obrigacao_acessoria.post("/obrigacao_acessoria/", response_model=schemas.ObrigacaoAcessoriaCreate, status_code=201)
def create_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, database: Session = Depends(get_db)):
    empresa_db = crud_empresa.get_empresa_by_id(database, empresa_id=obrigacao.empresa_id)
    if not empresa_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A empresa não existe.")
    return crud_obrigacao_acessoria.create_obrigacao_acessoria(database=database, obrigacao_acessoria=obrigacao)

@router_obrigacao_acessoria.get("/obrigacao_acessoria/", response_model=List[schemas.ObrigacaoAcessoria], status_code=200)
def get_obrigacao_acessoria(database: Session = Depends(get_db)):
    obrigacoes_db = crud_obrigacao_acessoria.get_obrigacao_acessoria_all(database=database)
    if not obrigacoes_db:
        return []
    return obrigacoes_db

@router_obrigacao_acessoria.get("/obrigacao_acessoria/{id}", response_model=schemas.ObrigacaoAcessoria, status_code=200)
def get_obrigacao_acessoria_unique(database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    obrigacao_acessoria_db = crud_obrigacao_acessoria.get_obrigacao_acessoria_by_id(database=database, obrigacao_id=id)
    if not obrigacao_acessoria_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada.")
    return obrigacao_acessoria_db

@router_obrigacao_acessoria.delete("/obrigacao_acessoria/{id}", response_model=schemas.ObrigacaoAcessoria, status_code=200)
def delete_obrigacao_acessoria(database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    obrigacao_acessoria_db = crud_obrigacao_acessoria.get_obrigacao_acessoria_by_id(database=database, obrigacao_id=id)
    if not obrigacao_acessoria_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada.")
    return crud_obrigacao_acessoria.delete_obrigacao_acessoria(database=database, obrigacao_id=id)

@router_obrigacao_acessoria.put("/obrigacao_acessoria/{id}", response_model=schemas.ObrigacaoAcessoria, status_code=200)
def update_obrigacao_acessoria(obrigacao_acessoria: schemas.ObrigacaoAcessoriaUpdate, database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    obrigacao_acessoria_db = crud_obrigacao_acessoria.get_obrigacao_acessoria_by_id(database=database, obrigacao_id=id)
    if not obrigacao_acessoria_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Obrigação acessória não encontrada.")
    return crud_obrigacao_acessoria.update_obrigacao_acessoria(database=database, obrigacao_id=id, obrigacao_update=obrigacao_acessoria)
