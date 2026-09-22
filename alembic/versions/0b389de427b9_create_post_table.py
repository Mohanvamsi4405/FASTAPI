"""Create Post Table

Revision ID: 0b389de427b9
Revises: 
Create Date: 2026-09-22 10:46:09.346337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b389de427b9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer,primary_key=True,nullable=False),
    sa.Column('title',sa.String,nullable=False),
    )

def downgrade() -> None:
    op.drop_table("posts")
