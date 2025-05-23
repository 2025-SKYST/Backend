"""create user table

Revision ID: d87b522ac0e7
Revises: c2356e0dcec5
Create Date: 2025-05-11 08:37:59.349692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd87b522ac0e7'
down_revision = 'c2356e0dcec5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocked_tokens',
    sa.Column('token_id', sa.String(length=255), nullable=False),
    sa.Column('expired_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('login_id', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('birth', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_login_id'), 'user', ['login_id'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('chapter',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('chapter_name', sa.String(length=100), nullable=False),
    sa.Column('prologue', sa.Text(), nullable=True),
    sa.Column('epilogue', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('main_image_url', sa.Text(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chapter_user_id'), 'chapter', ['user_id'], unique=False)
    op.create_table('image',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('file_url', sa.Text(), nullable=False),
    sa.Column('chapter_id', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('is_main', sa.Boolean(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapter.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    op.drop_index(op.f('ix_chapter_user_id'), table_name='chapter')
    op.drop_table('chapter')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_login_id'), table_name='user')
    op.drop_table('user')
    op.drop_table('blocked_tokens')
    # ### end Alembic commands ###
