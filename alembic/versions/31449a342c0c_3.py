"""3

Revision ID: 31449a342c0c
Revises: 5ce56d9d564c
Create Date: 2024-05-17 14:22:25.972180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31449a342c0c'
down_revision: Union[str, None] = '5ce56d9d564c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # # Convert latitude and longitude columns to floats for nodes
    # op.alter_column('nodes', 'latitude', type_=sa.Float, using='latitude::float')
    # op.alter_column('nodes', 'longitude', type_=sa.Float, using='longitude::float')

    # # Convert latitude and longitude columns to floats for anchors
    # op.alter_column('anchors', 'latitude', type_=sa.Float, using='latitude::float')
    # op.alter_column('anchors', 'longitude', type_=sa.Float, using='longitude::float')

    # # Convert latitude and longitude columns to floats for users
    # op.alter_column('users', 'latitude', type_=sa.Float, using='latitude::float')
    # op.alter_column('users', 'longitude', type_=sa.Float, using='longitude::float')
    pass


def downgrade():
    # # Convert latitude and longitude columns back to strings for nodes
    # op.alter_column('nodes', 'latitude', type_=sa.String(256))
    # op.alter_column('nodes', 'longitude', type_=sa.String(256))

    # # Convert latitude and longitude columns back to strings for anchors
    # op.alter_column('anchors', 'latitude', type_=sa.String(256))
    # op.alter_column('anchors', 'longitude', type_=sa.String(256))

    # # Convert latitude and longitude columns back to strings for users
    # op.alter_column('users', 'latitude', type_=sa.String(256))
    # op.alter_column('users', 'longitude', type_=sa.String(256))
    pass