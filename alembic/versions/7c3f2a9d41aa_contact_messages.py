"""contact_messages

Revision ID: 7c3f2a9d41aa
Revises: ed1e0bf5bedd
Create Date: 2026-07-10 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7c3f2a9d41aa'
down_revision: Union[str, None] = 'ed1e0bf5bedd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contact_messages',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('application', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contact_messages_application'), 'contact_messages', ['application'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_contact_messages_application'), table_name='contact_messages')
    op.drop_table('contact_messages')
