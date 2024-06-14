"""5

Revision ID: be5e5288424a
Revises: beeec24e239e
Create Date: 2024-05-24 14:59:30.797506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be5e5288424a'
down_revision: Union[str, None] = 'beeec24e239e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.drop_column('users', 'latitude')
    # op.drop_column('users', 'longitude')
    pass


def downgrade() -> None:
    # op.add_column('users', sa.Column('latitude', sa.Float, nullable=False))
    # op.add_column('users', sa.Column('longitude', sa.Float, nullable=False))
    pass
