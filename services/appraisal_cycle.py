# from sqlalchemy.orm import Session
# from dao.appraisal_cycle import get_all_cycles, get_cycle_by_id, create_cycle
from schema.appraisal_cycle_pydantic import AppraisalCycleCreate

from sqlalchemy.orm import Session
from dao.appraisal_cycle import create_cycle, get_all_cycles, get_cycle_by_id, get_all_cycles_with_stages, delete_cycle, get_completed_appraisal_cycles, get_completed_and_lead_assessment_active_cycles,get_completed_and_self_assessment_active_cycles

def add_new_cycle(db: Session, cycle_data: AppraisalCycleCreate):
    return create_cycle(db, cycle_data)

def fetch_all_cycles(db: Session):
    return get_all_cycles(db)

def fetch_cycle_by_id(db: Session, cycle_id: int):
    cycle = get_cycle_by_id(db, cycle_id)
    if not cycle:
        return None
    return cycle

def fetch_all_cycles_with_stages(db: Session):
    return get_all_cycles_with_stages(db)

def delete_appraisal_cycle(db: Session, cycle_id: int):
    return delete_cycle(db, cycle_id)

#for historical report

# def get_completed_cycles(db: Session):
#     return get_completed_appraisal_cycles(db)


def get_completed_cycles(db: Session):
    cycles = get_completed_and_lead_assessment_active_cycles(db)
    # if not cycle:
        # return None
    return cycles

def get_filtered_cycles(db: Session):
    cycles = get_completed_and_self_assessment_active_cycles(db)
    return cycles