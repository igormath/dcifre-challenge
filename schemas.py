from enum import Enum
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

class EmpresaCreate(BaseModel):
    nome: str
    cnpj: Annotated[ 
        str, 
        StringConstraints(
            strip_whitespace=True,
            min_length=14,
            max_length=14
        ),
    ]
    endereco: str
    email: EmailStr
    telefone: str

class Empresa(EmpresaCreate):
    id: int
    
    class Config:
        orm_mode = True

class Periodicidade(str, Enum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"

class ObrigacaoAcessoriaCreate(BaseModel):
    nome: str
    periodicidade: Periodicidade
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaCreate):
    id: int

    class Config:
        orm_mode: True
