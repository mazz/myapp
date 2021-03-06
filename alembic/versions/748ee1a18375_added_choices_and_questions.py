"""Added choices and questions

Revision ID: 748ee1a18375
Revises: d24bef47c0d8
Create Date: 2017-03-19 19:24:55.948680

"""

# revision identifiers, used by Alembic.
revision = '748ee1a18375'
down_revision = 'd24bef47c0d8'
branch_labels = None
depends_on = None

import datetime
import websauna.system.model.columns
from sqlalchemy.types import Text  # Needed from proper creation of JSON fields as Alembic inserts astext_type=Text() row

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('question_text', sa.String(length=256), nullable=True),
    sa.Column('published_at', websauna.system.model.columns.UTCDateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question'))
    )
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('choice_text', sa.String(length=256), nullable=True),
    sa.Column('votes', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_choice_question_id_question')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_choice'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choice')
    op.drop_table('question')
    # ### end Alembic commands ###
