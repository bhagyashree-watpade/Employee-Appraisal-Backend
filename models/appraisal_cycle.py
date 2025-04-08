
from database.connection import Base
from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.orm import relationship

  
class AppraisalCycle(Base):
    __tablename__ = "appraisal_cycle"  # Make sure the table name matches exactly

    cycle_id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)  # Nullable if the column allows NULL values
    start_date_of_cycle = Column(Date, nullable=False)
    end_date_of_cycle = Column(Date, nullable=False)
   

    # CHECK Constraint for status column
    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'completed')", name="check_status"),
    )

    stages = relationship("Stage", back_populates="cycle", cascade="all, delete")
     # Define One-to-Many Relationship
    parameters = relationship("Parameter", back_populates="cycle", cascade="all, delete-orphan")