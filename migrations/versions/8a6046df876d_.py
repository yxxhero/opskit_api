"""empty message

Revision ID: 8a6046df876d
Revises: 240062affe0c
Create Date: 2019-02-16 14:42:43.584911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a6046df876d'
down_revision = '240062affe0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_auditing', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_auditing')
    # ### end Alembic commands ###