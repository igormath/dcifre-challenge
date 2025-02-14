from sqlalchemy.orm import Session
import models, schemas

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

