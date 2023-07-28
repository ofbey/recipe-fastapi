"""add foreign key to recipes table

Revision ID: ef70e60b12da
Revises: 6a50c2c2d375
Create Date: 2023-07-27 21:47:36.495918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef70e60b12da'
down_revision = '6a50c2c2d375'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('recipe_users_fk', source_table="recipes", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('recipe_users_fk', table_name="recipes")
    pass