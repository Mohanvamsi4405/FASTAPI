"""Create Users table

Revision ID: da29447daacc
Revises: ceb58b493c56
Create Date: 2026-09-22 11:10:30.723951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da29447daacc'
down_revision: Union[str, None] = 'ceb58b493c56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id',sa.Integer,primary_key=True,nullable=False),
    sa.Column('email',sa.String,nullable=False,unique=True),
    sa.Column('password',sa.String,nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )

def downgrade() -> None:
    op.drop_table('users')
