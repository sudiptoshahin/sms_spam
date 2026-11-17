"""report: create report table

Revision ID: b5e4d4bf9b8a
Revises: 
Create Date: 2026-11-16 12:07:37.032760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision: str = 'b5e4d4bf9b8a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'reports',
        sa.Column('id', sa.String(32), primary_key=True, default=lambda: uuid.uuid4().hex),
        sa.Column('label', sa.String(5), nullable=False),
        sa.Column('message', sa.String(255), nullable=False),
        sa.Column('percentage', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('reports')
    pass
