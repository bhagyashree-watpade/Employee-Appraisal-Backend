from database.connection import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class QuestionAssignment(Base):
    __tablename__ = "assigned_questions"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employee.employee_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.question_id", ondelete="CASCADE"), nullable=False)
    cycle_id = Column(Integer, ForeignKey("appraisal_cycle.cycle_id", ondelete="CASCADE"), nullable=False)

    employee = relationship("Employee")
    question = relationship("Question")
    cycle = relationship("AppraisalCycle")
