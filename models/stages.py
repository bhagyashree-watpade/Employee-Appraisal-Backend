
from database.connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Stage(Base):
    __tablename__ = "stages"

    stage_id = Column(Integer, primary_key=True, autoincrement=True)
    stage_name = Column(String(50), nullable=False)
    cycle_id = Column(Integer, ForeignKey("appraisal_cycle.cycle_id", ondelete="CASCADE"), nullable=True)
    start_date_of_stage = Column(Date, nullable=True)
    end_date_of_stage = Column(Date, nullable = True)
    
    cycle = relationship("AppraisalCycle", back_populates="stages")