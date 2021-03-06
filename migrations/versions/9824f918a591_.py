"""empty message

Revision ID: 9824f918a591
Revises: 6f17eddd81cf
Create Date: 2021-12-01 20:30:36.670296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9824f918a591'
down_revision = '6f17eddd81cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attendance', sa.Column('attendance_date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('attendance', 'attendance_date')
    # ### end Alembic commands ###
