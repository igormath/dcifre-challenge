from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    cnpj = Column(String(14), unique=True, nullable=False, index=True)
    endereco = Column(String(100), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    telefone = Column(String(15), nullable=False, index=True)

class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    periodicidade = Column(String(20), nullable=False, index=True) # Lembrar de Adicionar ENUM no pydantic depois (mensal, trimestral ou anual)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False, index=True)
    empresa = relationship("Empresa") # Manter dessa forma por enquanto. Mais pra frente, se for o caso, analisar back populates e back ref.
