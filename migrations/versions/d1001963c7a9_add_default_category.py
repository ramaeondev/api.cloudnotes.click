"""Add default category

Revision ID: d1001963c7a9
Revises: efdb28a80f4f
Create Date: 2025-02-28 10:04:50.438848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import ulid


# revision identifiers, used by Alembic.
revision: str = 'd1001963c7a9'
down_revision: Union[str, None] = 'efdb28a80f4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
DEFAULT_CATEGORY_ID = ulid.new().str


def upgrade() -> None:
    op.execute(f"""
        INSERT INTO categories (id, user_id, name, color, created_at)
        VALUES ('{DEFAULT_CATEGORY_ID}', NULL, 'Uncategorized', '#FFFFFF', NOW())
        ON CONFLICT (id) DO NOTHING;
    """)

def downgrade() -> None:
     op.execute(f"DELETE FROM categories WHERE id = '{DEFAULT_CATEGORY_ID}';")
