"""primeira_migracao

Revision ID: d46f73e172d2
Revises: 
Create Date: 2025-02-14 16:20:05.909287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd46f73e172d2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "empresas",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("nome", sa.String(100), nullable=False, index=True),
        sa.Column("cnpj", sa.String(14), unique=True, nullable=False, index=True),
        sa.Column("endereco", sa.String(100), nullable=False, index=True),
        sa.Column("email", sa.String(50), nullable=False, index=True),
        sa.Column("telefone", sa.String(15), nullable=False, index=True),
    )

    op.create_table(
        "obrigacoes_acessorias",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("nome", sa.String(100), nullable=False, index=True),
        sa.Column("periodicidade", sa.String(20), nullable=False, index=True),
        sa.Column("empresa_id", sa.Integer, sa.ForeignKey("empresas.id"), nullable=False, index=True),
    )


def downgrade():
    op.drop_table("obrigacoes_acessorias")
    op.drop_table("empresas")
