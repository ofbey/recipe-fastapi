"""create steps table

Revision ID: 89e5a4767ece
Revises: d311c1f9cfac
Create Date: 2023-07-27 21:21:02.340837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89e5a4767ece'
down_revision = 'd311c1f9cfac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'steps',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('recipe_id', sa.Integer),
        sa.Column('step', sa.String),
        sa.Column('step_number', sa.Integer),
    )
    op.create_foreign_key('step_recipe_fk', source_table="steps", referent_table="recipes", local_cols=[
                          'recipe_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('step_recipe_fk', table_name="steps")
    op.drop_table('steps')
