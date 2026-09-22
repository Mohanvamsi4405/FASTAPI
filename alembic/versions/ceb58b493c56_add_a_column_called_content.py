"""Add a column called Content

Revision ID: ceb58b493c56
Revises: 0b389de427b9
Create Date: 2026-09-22 10:59:18.662107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ceb58b493c56'
down_revision: Union[str, None] = '0b389de427b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
