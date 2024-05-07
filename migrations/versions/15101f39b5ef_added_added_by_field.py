"""added added_by field

Revision ID: 15101f39b5ef
Revises: 
Create Date: 2024-05-07 11:11:37.327728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15101f39b5ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('opinion', sa.Column('added_by', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('opinion', 'added_by')
    # ### end Alembic commands ###