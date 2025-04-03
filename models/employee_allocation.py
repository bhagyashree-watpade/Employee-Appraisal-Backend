from database.connection import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class EmployeeAllocation(Base):
    __tablename__ = "employee_allocation"

    allocation_id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_id = Column(Integer, ForeignKey("appraisal_cycle.cycle_id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.employee_id", ondelete="CASCADE"), nullable=False)

    employee = relationship("Employee")
    cycle = relationship("AppraisalCycle")
