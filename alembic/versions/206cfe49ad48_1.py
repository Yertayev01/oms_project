"""1

Revision ID: 206cfe49ad48
Revises: 5e7f2a9a6d9c
Create Date: 2024-05-17 11:22:35.743858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '206cfe49ad48'
down_revision: Union[str, None] = '5e7f2a9a6d9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # # Drop unique constraints
    # with op.batch_alter_table('nodes') as batch_op:
    #     batch_op.drop_constraint('uq_nodes_node_title', type_='unique')
    # with op.batch_alter_table('anchors') as batch_op:
    #     batch_op.drop_constraint('uq_anchor_anchor_title', type_='unique')
    # with op.batch_alter_table('objects') as batch_op:
    #     batch_op.drop_constraint('uq_objects_object_title', type_='unique')

    # # # Update columns (unique=False is the default, so we don't need to specify it)
    # # with op.batch_alter_table('nodes') as batch_op:
    # #     batch_op.alter_column('node_title', existing_type=sa.String(256), nullable=False)
    # # with op.batch_alter_table('anchors') as batch_op:
    # #     batch_op.alter_column('anchor_title', existing_type=sa.String(256), nullable=False)
    # # with op.batch_alter_table('objects') as batch_op:
    # #     batch_op.alter_column('object_title', existing_type=sa.String(256), nullable=False)
    pass

def downgrade() -> None:
    # # Revert the column changes and add back unique constraints
    # with op.batch_alter_table('nodes') as batch_op:
    #     batch_op.alter_column('node_title', existing_type=sa.String(256), nullable=False)
    #     batch_op.create_unique_constraint('uq_nodes_node_title', ['node_title'])
    # with op.batch_alter_table('anchors') as batch_op:
    #     batch_op.alter_column('anchor_title', existing_type=sa.String(256), nullable=False)
    #     batch_op.create_unique_constraint('uq_anchor_anchor_title', ['anchor_title'])
    # with op.batch_alter_table('objects') as batch_op:
    #     batch_op.alter_column('object_title', existing_type=sa.String(256), nullable=False)
    #     batch_op.create_unique_constraint('uq_objects_object_title', ['object_title'])
    pass