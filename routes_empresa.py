from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
import crud_empresa, models, schemas
from db import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)
router_empresa = APIRouter()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@router_empresa.post("/empresa/", response_model=schemas.Empresa, status_code=201)
def create_empresa(empresa: schemas.EmpresaCreate, database: Session = Depends(get_db)):
    db_empresa_exists = crud_empresa.get_empresa_by_cnpj(database, empresa_cnpj=empresa.cnpj)
    if db_empresa_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A empresa já está cadastrada.")
    return crud_empresa.create_empresa(database=database, empresa=empresa)

@router_empresa.get("/empresa/", response_model=List[schemas.Empresa], status_code=200)
def get_empresa(database: Session = Depends(get_db)):
    empresa = crud_empresa.get_empresa_all(database=database)
    if not empresa:
        return []
    return empresa

@router_empresa.get("/empresa/{id}/", response_model=schemas.Empresa, status_code=200)
def get_empresa_unique(database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    db_empresa = crud_empresa.get_empresa_by_id(database, id)
    if not db_empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A empresa não existe no cadastro.")
    return db_empresa

@router_empresa.delete("/empresa/{id}", response_model=schemas.Empresa, status_code=200)
def delete_empresa(database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    db_empresa = crud_empresa.get_empresa_by_id(database, id)
    if not db_empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada.")
    return crud_empresa.delete_empresa(database=database, empresa_id=id)

@router_empresa.put("/empresa/{id}", response_model=schemas.Empresa, status_code=200)
def put_empresa(empresa: schemas.EmpresaUpdate, database: Session = Depends(get_db), id: int = Path(..., gt=0)):
    db_empresa = crud_empresa.get_empresa_by_id(database, id)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="A empresa não existe no cadastro.")
    return crud_empresa.update_empresa(database=database, empresa_id=id, empresa=empresa)
