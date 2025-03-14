"""Initial migration

Revision ID: 194cfe3cc29a
Revises: 
Create Date: 2025-03-14 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '194cfe3cc29a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop the existing foreign key constraint on notes.category_id
    op.drop_constraint('notes_category_id_fkey', 'notes', type_='foreignkey')
    
    # Alter notes.category_id column type from INTEGER to VARCHAR(26)
    op.alter_column('notes', 'category_id',
               existing_type=sa.Integer(),
               type_=sa.String(length=26),
               existing_nullable=True)
    
    # Re-create the foreign key constraint referencing categories.id (a string column)
    op.create_foreign_key(
        'notes_category_id_fkey',    # constraint name
        'notes',                     # source table
        'categories',                # referent table
        ['category_id'],             # local column(s)
        ['id'],                      # remote column(s) (the ULID string column)
        ondelete='SET NULL'
    )

def downgrade():
    # In the downgrade, reverse the operations
    op.drop_constraint('notes_category_id_fkey', 'notes', type_='foreignkey')
    
    # Change the column back from VARCHAR(26) to INTEGER
    op.alter_column('notes', 'category_id',
               existing_type=sa.String(length=26),
               type_=sa.Integer(),
               existing_nullable=True)
    
    # Re-create the original foreign key constraint referencing categories.numeric_id
    op.create_foreign_key(
        'notes_category_id_fkey',
        'notes',
        'categories',
        ['category_id'],
        ['numeric_id'],
        ondelete='SET NULL'
    )
