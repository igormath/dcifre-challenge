from sqlalchemy.orm import Session
import models, schemas

def create_obrigacao_acessoria(db: Session, obrigacao_acessoria: schemas.ObrigacaoAcessoriaCreate, empresa_fk: int):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao_acessoria.model_dump(), empresa_id=empresa_fk)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

