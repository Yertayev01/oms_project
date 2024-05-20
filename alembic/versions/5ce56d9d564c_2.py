"""2

Revision ID: 5ce56d9d564c
Revises: 206cfe49ad48
Create Date: 2024-05-17 11:36:15.733112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '5ce56d9d564c'
down_revision: Union[str, None] = '206cfe49ad48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # # Get the connection and inspector
    # conn = op.get_bind()
    # inspector = Inspector.from_engine(conn)

    # # Nodes table
    # constraints = inspector.get_unique_constraints('nodes')
    # for constraint in constraints:
    #     if 'node_title' in constraint['column_names']:
    #         op.drop_constraint(constraint['name'], 'nodes', type_='unique')
    #         break

    # # Anchors table
    # constraints = inspector.get_unique_constraints('anchors')
    # for constraint in constraints:
    #     if 'anchor_title' in constraint['column_names']:
    #         op.drop_constraint(constraint['name'], 'anchors', type_='unique')
    #         break

    # # Objects table
    # constraints = inspector.get_unique_constraints('objects')
    # for constraint in constraints:
    #     if 'object_title' in constraint['column_names']:
    #         op.drop_constraint(constraint['name'], 'objects', type_='unique')
    #         break
    pass

def downgrade() -> None:
    # # Recreate unique constraint for nodes.node_title
    # op.create_unique_constraint('uq_nodes_node_title', 'nodes', ['node_title'])
    
    # # Recreate unique constraint for anchors.anchor_title
    # op.create_unique_constraint('uq_anchors_anchor_title', 'anchors', ['anchor_title'])
    
    # # Recreate unique constraint for objects.object_title
    # op.create_unique_constraint('uq_objects_object_title', 'objects', ['object_title'])
    pass