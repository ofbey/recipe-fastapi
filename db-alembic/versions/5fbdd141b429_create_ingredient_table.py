"""create ingredient table

Revision ID: 5fbdd141b429
Revises: 80e66dfd03c8
Create Date: 2023-07-27 21:12:02.817721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fbdd141b429'
down_revision = '80e66dfd03c8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ingredients',
        sa.Column('id', sa.Integer),
        sa.Column('recipe_id', sa.Integer),
        sa.Column('ingredient', sa.String),
        sa.Column('ingredient_number', sa.Integer),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_foreign_key('ingredient_recipe_fk', source_table="ingredients", referent_table="recipes", local_cols=[
                          'recipe_id'], remote_cols=['id'], ondelete="CASCADE")

def downgrade():
    op.drop_constraint('ingredient_recipe_fk', table_name="ingredients")
    op.drop_table('ingredients')
