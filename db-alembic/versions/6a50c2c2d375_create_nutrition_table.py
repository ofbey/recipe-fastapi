"""create nutrition table

Revision ID: 6a50c2c2d375
Revises: 89e5a4767ece
Create Date: 2023-07-27 21:22:40.414943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a50c2c2d375'
down_revision = '89e5a4767ece'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'nutritions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('recipe_id', sa.Integer),
        sa.Column('calories', sa.Float),
        sa.Column('total_fat', sa.Float),
        sa.Column('sugar', sa.Float),
        sa.Column('sodium', sa.Float),
        sa.Column('protein', sa.Float),
        sa.Column('saturated_fat', sa.Float),
        sa.Column('carbohydrates', sa.Float),
    )
    op.create_foreign_key('nutrition_recipe_fk', source_table="nutritions", referent_table="recipes", local_cols=[
                          'recipe_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('nutrition_recipe_fk', table_name="nutritions")
    op.drop_table('nutritions')

