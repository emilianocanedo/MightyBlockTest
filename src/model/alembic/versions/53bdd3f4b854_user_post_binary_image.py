"""User post binary image

Revision ID: 53bdd3f4b854
Revises: 8279d6fd6a37
Create Date: 2021-08-05 16:13:29.839839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53bdd3f4b854'
down_revision = '8279d6fd6a37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userpost', sa.Column('image', sa.LargeBinary(), nullable=True))
    op.drop_column('userpost', 'image_path')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userpost', sa.Column('image_path', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('userpost', 'image')
    # ### end Alembic commands ###
