"""auto_rep

Revision ID: 51a5d7582790
Revises: 17346fa73e70
Create Date: 2024-10-16 22:51:43.826966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51a5d7582790'
down_revision: Union[str, None] = '17346fa73e70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('auto_reply_enabled', sa.Boolean(), nullable=True))
    op.add_column('posts', sa.Column('auto_reply_delay', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'auto_reply_delay')
    op.drop_column('posts', 'auto_reply_enabled')
    # ### end Alembic commands ###
