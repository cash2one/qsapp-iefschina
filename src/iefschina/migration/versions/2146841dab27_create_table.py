"""create_table

Revision ID: 2146841dab27
Revises: None
Create Date: 2014-10-28 17:50:05.827101

"""

# revision identifiers, used by Alembic.
revision = '2146841dab27'
down_revision = None


from sqlalchemy import sql
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        u'navi',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.Unicode(64), nullable=False, unique=True, index=True),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'channel',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('channel.id'), index=True),
        sa.Column('name', sa.Unicode(64), nullable=False, unique=True, index=True),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'navi_channel',
        sa.Column('navi_id', sa.Integer(), sa.ForeignKey('navi.id'), primary_key=True, index=True),
        sa.Column('channel_id', sa.Integer(), sa.ForeignKey('channel.id'), primary_key=True, index=True),
    )

    op.create_table(
        u'channel_summary',
        sa.Column('id', sa.Integer(), sa.ForeignKey('channel.id'),
                    nullable=False, primary_key=True),
        sa.Column('content', sa.UnicodeText(), nullable=False),
    )

    op.create_table(
        u'slide',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.Unicode(256), nullable=True, index=True),
        sa.Column('describe', sa.Unicode(1024), nullable=True, index=True),
        sa.Column('order', sa.Integer(), nullable=False, index=True),
        sa.Column('image', sa.Unicode(length=2083), nullable=False),
        sa.Column('link', sa.Unicode(length=2083), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'article',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('channel_id', sa.Integer(), nullable=False, index=True),
        sa.Column('is_sticky', sa.Boolean(),
                    server_default=sql.false(), nullable=False),
        sa.Column('title', sa.Unicode(64), nullable=False, unique=True, index=True),
        sa.Column('date_published', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
        sa.Column('date_created', sa.DateTime(timezone=True),
                    nullable=False, index=True,
                    server_default=sa.func.current_timestamp()),
    )

    op.create_table(
        u'article_content',
        sa.Column('id', sa.Integer(), sa.ForeignKey('article.id'),
                    nullable=False, primary_key=True),
        sa.Column('content', sa.UnicodeText(), nullable=False),
    )


def downgrade():
    op.drop_table(u'article_content')
    op.drop_table(u'article')
    op.drop_table(u'slide')
    op.drop_table(u'channel_summary')
    op.drop_table(u'navi_channel')
    op.drop_table(u'channel')
    op.drop_table(u'navi')
