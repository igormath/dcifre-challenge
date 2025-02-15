from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud_obrigacao_acessoria, models, schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
router_obrigacao_acessoria = APIRouter()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@router_obrigacao_acessoria.post("/obrigacao_acessoria/", response_model=schemas.ObrigacaoAcessoriaCreate)
def create_empresa(obrigacao: schemas.ObrigacaoAcessoriaCreate, database: Session = Depends(get_db)):
    db_obrigacao = crud_obrigacao_acessoria.get_obrigacao_acessoria_by_id(database, obrigacao_id=obrigacao.id)
    if db_obrigacao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A obrigação já está cadastrada")
    return crud_obrigacao_acessoria.create_obrigacao_acessoria(database=database, obrigacao=obrigacao)
