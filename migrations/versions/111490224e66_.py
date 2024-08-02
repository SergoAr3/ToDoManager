"""

Revision ID: 111490224e66
Revises: 
Create Date: 2024-08-02 13:22:12.074222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '111490224e66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    access_type_table = op.create_table('access_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=15), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )

    op.bulk_insert(
        access_type_table,
        [
            {'id': 1, 'type': 'read only'},
            {'id': 2, 'type': 'editor'}
        ]
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('hashed_password', sa.LargeBinary(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_owner_id'), 'task', ['owner_id'], unique=False)
    op.create_table('task_access',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('access_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['access_id'], ['access_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_access_access_id'), 'task_access', ['access_id'], unique=False)
    op.create_index(op.f('ix_task_access_task_id'), 'task_access', ['task_id'], unique=False)
    op.create_index(op.f('ix_task_access_user_id'), 'task_access', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_access_user_id'), table_name='task_access')
    op.drop_index(op.f('ix_task_access_task_id'), table_name='task_access')
    op.drop_index(op.f('ix_task_access_access_id'), table_name='task_access')
    op.drop_table('task_access')
    op.drop_index(op.f('ix_task_owner_id'), table_name='task')
    op.drop_table('task')
    op.drop_table('user')
    op.drop_table('access_type')
    # ### end Alembic commands ###
