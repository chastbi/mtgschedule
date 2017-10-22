"""empty message

Revision ID: 4880c1a7e107
Revises: 0ea59f0ba6b6
Create Date: 2017-10-01 13:44:55.186630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4880c1a7e107'
down_revision = '0ea59f0ba6b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('mtg_time2', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedule', 'mtg_time2')
    # ### end Alembic commands ###