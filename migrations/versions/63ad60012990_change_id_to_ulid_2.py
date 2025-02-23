"""Change ID to ULID-2

Revision ID: 63ad60012990
Revises: fe1788eb3490
Create Date: 2025-02-23 19:27:07.518930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63ad60012990'
down_revision: Union[str, None] = 'fe1788eb3490'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("integer_id", sa.Integer(), nullable=False))

    # Create a sequence starting from 1001
    op.execute("CREATE SEQUENCE users_integer_id_seq START WITH 1001;")
    
    # Set default value using the sequence
    op.execute("ALTER TABLE users ALTER COLUMN integer_id SET DEFAULT nextval('users_integer_id_seq');")

    # Add a unique constraint to prevent duplicates
    op.create_unique_constraint("uq_users_integer_id", "users", ["integer_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_integer_id", "users", type_="unique")
    op.drop_column("users", "integer_id")
    op.execute("DROP SEQUENCE IF EXISTS users_integer_id_seq;")