"""4

Revision ID: beeec24e239e
Revises: 31449a342c0c
Create Date: 2024-05-20 15:50:12.833049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beeec24e239e'
down_revision: Union[str, None] = '31449a342c0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.alter_column('videos', 'video_thumb_name',
    #                 existing_type=sa.String(length=256),
    #                 nullable=True)
    pass


def downgrade() -> None:
    # op.alter_column('videos', 'video_thumb_name',
    #                 existing_type=sa.String(length=256),
    #                 nullable=False)
    pass