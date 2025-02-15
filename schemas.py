from enum import Enum
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

class EmpresaBase(BaseModel):
    nome: str
    endereco: str
    email: EmailStr
    telefone: str

class EmpresaCreate(EmpresaBase):
    cnpj: Annotated[ 
        str, 
        StringConstraints(
            strip_whitespace=True,
            min_length=14,
            max_length=14
        ),
    ]

class EmpresaUpdate(EmpresaBase):
    cnpj: Annotated[ 
        str, 
        StringConstraints(
            strip_whitespace=True,
            min_length=14,
            max_length=14
        ),
    ] | None = None

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
