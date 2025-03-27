from sqlalchemy.orm import Session
from models.appraisal_cycle import AppraisalCycle
from schema.appraisal_cycle_pydantic import AppraisalCycleCreate

def create_cycle(db: Session, cycle_data: AppraisalCycleCreate):
    new_cycle = AppraisalCycle(
        cycle_name=cycle_data.cycle_name,
        description=cycle_data.description,
        status=cycle_data.status,  # Must be 'active' or 'inactive'
        start_date_of_cycle=cycle_data.start_date_of_cycle,
        end_date_of_cycle=cycle_data.end_date_of_cycle
    )
    db.add(new_cycle)
    db.commit()
    db.refresh(new_cycle)  # Return updated cycle with ID
    return new_cycle

def get_all_cycles(db: Session):
    return db.query(AppraisalCycle).all()

def get_cycle_by_id(db: Session, cycle_id: int):
    return db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()
