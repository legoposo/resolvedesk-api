"""add role to users

Revision ID: 6e70169836eb
Revises: 23789b2c5e32
Create Date: 2026-09-16 16:35:12.496444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e70169836eb'
down_revision: Union[str, Sequence[str], None] = '23789b2c5e32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=20),
            nullable=False,
            server_default='USER',
        )
    )


def downgrade() -> None:
    op.drop_column('users', 'role')
    
