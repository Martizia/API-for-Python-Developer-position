"""auto_rep

Revision ID: 4c57500bc0f7
Revises: 51a5d7582790
Create Date: 2024-10-16 22:55:26.867692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c57500bc0f7'
down_revision: Union[str, None] = '51a5d7582790'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'auto_reply_delay',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'auto_reply_delay',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
