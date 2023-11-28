"""empty message

Revision ID: f28197ce455c
Revises: b58f2f0c0912
Create Date: 2023-11-27 11:04:50.872345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f28197ce455c'
down_revision = 'b58f2f0c0912'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cpf', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('senha', sa.String(length=255), nullable=False))
        batch_op.drop_constraint('usuarios_email_key', type_='unique')
        batch_op.create_unique_constraint(None, ['cpf'])
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('usuarios_email_key', ['email'])
        batch_op.drop_column('senha')
        batch_op.drop_column('cpf')

    # ### end Alembic commands ###
