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
        from_attributes = True

class Periodicidade(str, Enum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: Periodicidade

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoriaUpdate(ObrigacaoAcessoriaBase):
    nome: str | None = None
    periodicidade: Periodicidade | None = None

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    class Config:
        from_attributes: True
