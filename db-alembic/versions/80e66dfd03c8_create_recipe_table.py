"""create recipe table

Revision ID: 80e66dfd03c8
Revises: b8c3530d6081
Create Date: 2023-07-27 21:05:50.091853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80e66dfd03c8'
down_revision = 'b8c3530d6081'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String),
        sa.Column('minutes', sa.Integer),
        sa.Column('n_steps', sa.Integer),
        sa.Column('description', sa.String),
        sa.Column('n_ingredients', sa.Integer),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )
    op.create_foreign_key('recipe_users_fk', source_table="recipes", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('recipe_users_fk', table_name="recipes")
    op.drop_table('recipes')
    pass