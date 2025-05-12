from sqlalchemy.orm import Session
from models.appraisal_cycle import AppraisalCycle
from models.stages import Stage
from models.parameters import Parameter
from schema.appraisal_cycle_pydantic import AppraisalCycleCreate, AppraisalCycleResponse, StageResponse, AppraisalCycleResponseWithStages
from collections import defaultdict
from fastapi import HTTPException
from sqlalchemy import or_, and_
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


def get_all_cycles_with_stages(db: Session):
    # Query to fetch cycle and stage details
    cycles = db.query(
        AppraisalCycle.cycle_id,
        AppraisalCycle.cycle_name,
        AppraisalCycle.description,
        AppraisalCycle.status,
        AppraisalCycle.start_date_of_cycle,
        AppraisalCycle.end_date_of_cycle,
        Stage.stage_name,
        Stage.start_date_of_stage,
        Stage.end_date_of_stage
    ).join(Stage, AppraisalCycle.cycle_id == Stage.cycle_id, isouter=True).all()

    # Dictionary to group cycles and their stages
    cycle_dict = defaultdict(lambda: {
        "cycle_id": None,
        "cycle_name": None,
        "description": None,
        "status": None,
        "start_date_of_cycle": None,
        "end_date_of_cycle": None,
        "stages": []
    })

    for cycle in cycles:
        cycle_data = cycle_dict[cycle.cycle_id]

        if cycle_data["cycle_id"] is None:
            cycle_data.update({
                "cycle_id": cycle.cycle_id,
                "cycle_name": cycle.cycle_name,
                "description": cycle.description,
                "status": cycle.status,
                "start_date_of_cycle": cycle.start_date_of_cycle,
                "end_date_of_cycle": cycle.end_date_of_cycle,
                "stages": []
            })

        if cycle.stage_name:  # Avoid adding None stages (in case of no stages)
            cycle_data["stages"].append(StageResponse(
                stage_name=cycle.stage_name,
                start_date_of_stage=cycle.start_date_of_stage,
                end_date_of_stage=cycle.end_date_of_stage
            ))

    # Convert dictionary values into response objects
    return [AppraisalCycleResponseWithStages(**cycle_data) for cycle_data in cycle_dict.values()]


def delete_cycle(db: Session, cycle_id: int):
    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()

    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    
    # Prevent deletion if the status is 'active' or 'completed'
    if cycle.status in ['active', 'completed']:
        raise HTTPException(status_code=400, detail="Cannot delete an active or completed cycle.")
    
    db.query(Stage).filter(Stage.cycle_id == cycle_id).delete()
    db.query(Parameter).filter(Parameter.cycle_id == cycle_id).delete()

    db.delete(cycle)
    db.commit()
    return {"message":"Cycle and related stages deleted successfully"}


#get all cycles which are completed and active ie. status not equal to inactive
def get_completed_appraisal_cycles(db: Session):
    return db.query(AppraisalCycle).filter(AppraisalCycle.status != "inactive").all()


def get_completed_and_lead_assessment_active_cycles(db: Session):
    return db.query(AppraisalCycle).join(Stage, AppraisalCycle.cycle_id == Stage.cycle_id)\
        .filter(
            or_(
                AppraisalCycle.status == "completed",
                and_(
                    AppraisalCycle.status == "active",
                    Stage.stage_name == "Lead Assessment",
                    or_(
                        Stage.is_active == True,
                        Stage.is_completed == True
                    )
                )
            )
        ).distinct().all()

#get all cycles which are completed and active cycles for which self assessment stage is active or completed (for self assessment report)

def get_completed_and_self_assessment_active_cycles(db: Session):
    return db.query(AppraisalCycle).join(Stage, AppraisalCycle.cycle_id==Stage.cycle_id)\
        .filter(
            or_(
                AppraisalCycle.status == "completed",
                and_(
                    AppraisalCycle.status == "active",
                        Stage.stage_name == "Self Assessment",
                        or_(
                            Stage.is_active == True,
                            Stage.is_completed == True
                        )
                )
            )
    ).distinct().all()