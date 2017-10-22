"""empty message

Revision ID: a6a4005a1977
Revises: a94687ef9521
Create Date: 2017-09-30 15:46:56.822923

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6a4005a1977'
down_revision = 'a94687ef9521'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('presenters',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_table('schedule',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('title', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('mtg_time1', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mtg_time2', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mtg_time3', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mtg_time4', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mtg_time5', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('mtg_topic1', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('mtg_topic2', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('mtg_topic3', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('mtg_topic4', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('mtg_topic5', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('notes', mysql.VARCHAR(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
