"""Initial migration

Revision ID: 4452b1eceb9c
Revises: 
Create Date: 2025-04-07 14:52:32.240076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '4452b1eceb9c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('self_assessment_response')
    op.alter_column('appraisal_cycle', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('assigned_questions', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('assigned_questions', 'question_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('assigned_questions', 'cycle_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('assigned_questions_cycle_id_employee_id_question_id_key', 'assigned_questions', type_='unique')
    op.alter_column('employee', 'role',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.create_index(op.f('ix_employee_employee_id'), 'employee', ['employee_id'], unique=False)
    op.alter_column('employee_allocation', 'cycle_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('employee_allocation', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('lead_assessment_rating', 'parameter_rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_lead_assessment_rating_lead_rating_id'), 'lead_assessment_rating', ['lead_rating_id'], unique=False)
    op.alter_column('stages', 'start_date_of_stage',
               existing_type=sa.DATE(),
               nullable=True)
    op.alter_column('stages', 'end_date_of_stage',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stages', 'end_date_of_stage',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('stages', 'start_date_of_stage',
               existing_type=sa.DATE(),
               nullable=False)
    op.drop_index(op.f('ix_lead_assessment_rating_lead_rating_id'), table_name='lead_assessment_rating')
    op.alter_column('lead_assessment_rating', 'parameter_rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('employee_allocation', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('employee_allocation', 'cycle_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_employee_employee_id'), table_name='employee')
    op.alter_column('employee', 'role',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.create_unique_constraint('assigned_questions_cycle_id_employee_id_question_id_key', 'assigned_questions', ['cycle_id', 'employee_id', 'question_id'])
    op.alter_column('assigned_questions', 'cycle_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('assigned_questions', 'question_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('assigned_questions', 'employee_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('appraisal_cycle', 'status',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.create_table('self_assessment_response',
    sa.Column('response_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('allocation_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cycle_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('option_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('response_text', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['allocation_id'], ['employee_allocation.allocation_id'], name='self_assessment_response_allocation_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['cycle_id'], ['appraisal_cycle.cycle_id'], name='self_assessment_response_cycle_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.employee_id'], name='self_assessment_response_employee_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['option_id'], ['option.option_id'], name='self_assessment_response_option_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['question_id'], ['question.question_id'], name='self_assessment_response_question_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('response_id', name='self_assessment_response_pkey')
    )
    # ### end Alembic commands ###
