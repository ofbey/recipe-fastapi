"""create tags table

Revision ID: d311c1f9cfac
Revises: 5fbdd141b429
Create Date: 2023-07-27 21:16:19.859626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd311c1f9cfac'
down_revision = '5fbdd141b429'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('recipe_id', sa.Integer),
        sa.Column('tag', sa.String),
        sa.Column('tag_number', sa.Integer),
    )
    op.create_foreign_key('tag_recipe_fk', source_table="tags", referent_table="recipes", local_cols=[
                          'recipe_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('tag_recipe_fk', table_name="tags")
    op.drop_table('tags')
