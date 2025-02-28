"""Insert default category

Revision ID: dbacbe3fde2d
Revises: a2fbed347fc4
Create Date: 2025-02-28 10:12:36.276035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import ulid


# revision identifiers, used by Alembic.
revision: str = 'dbacbe3fde2d'
down_revision: Union[str, None] = 'a2fbed347fc4'
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

