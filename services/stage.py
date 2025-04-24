from sqlalchemy.orm import Session
from datetime import date
from datetime import datetime
from sqlalchemy.orm import Session
from models.stages import Stage
from models.appraisal_cycle import AppraisalCycle
from dao.stage import get_all_stages, create_stage, get_self_assessment_stage_by_cycle_id, get_lead_assessment_stage_by_cycle_id
from schema.stage import StageCreate, StageInfoResponse
from fastapi import HTTPException

# Get all stages
def fetch_all_stages(db: Session):
    return get_all_stages(db)

# Add a new stage
def add_new_stage(db: Session, stage_data: StageCreate):
    return create_stage(db, stage_data)


# To update the cycle stages automatically using APSchedular
def update_current_stage(db: Session):
    today = datetime.utcnow().date()
    # print("Today (UTC):", today)

    # 1) Mark all completed stages (regardless of cycle status)
    all_stages = db.query(Stage).all()
    for stage in all_stages:
        # Reset active stage
        stage.is_active = False

        if stage.end_date_of_stage < today:
            if not stage.is_completed:
                stage.is_completed = True
                print(f"Marked stage '{stage.stage_name}' as completed (cycle_id={stage.cycle_id})")
        else:
            stage.is_completed = False  # Optional: reset if needed

    # 2)
    # Get all active cycles
    active_cycles = db.query(AppraisalCycle).filter(
        AppraisalCycle.status == "active"
    ).all()

    # print(f"Found {len(active_cycles)} active cycle(s)")

    for cycle in active_cycles:
        # print(f"Checking cycle {cycle.cycle_id}: {cycle.cycle_name} ({cycle.start_date_of_cycle} to {cycle.end_date_of_cycle})")

        # Find the stage(s) for this cycle valid today
        stages_today = db.query(Stage).filter(
            Stage.cycle_id == cycle.cycle_id,
            Stage.start_date_of_stage <= today,
            Stage.end_date_of_stage >= today
        ).order_by(Stage.start_date_of_stage.asc()).all()

        if stages_today:
            stage = stages_today[0]  # take the first (earliest-starting) one
            stage.is_active = True
            # print(f"Activated stage: {stage.stage_name} in cycle {cycle.cycle_id}")

         # === 3. Check if all stages in this cycle are completed ===
        cycle_stages = db.query(Stage).filter(Stage.cycle_id == cycle.cycle_id).all()
        if all(stage.is_completed for stage in cycle_stages):
            cycle.status = "completed"
            print(f" Marked cycle '{cycle.cycle_name}' as completed")

    db.commit()

def fetch_self_assessment_stage_info(cycle_id: int, db: Session) -> StageInfoResponse:
    stage = get_self_assessment_stage_by_cycle_id(db, cycle_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Self Assessment stage not found for the given cycle ID")
    
    return StageInfoResponse(
        start_date_of_stage=stage.start_date_of_stage,
        end_date_of_stage=stage.end_date_of_stage,
        is_active=stage.is_active,
        is_completed=stage.is_completed
        
    )
    
def fetch_lead_assessment_stage_info(cycle_id: int, db: Session) -> StageInfoResponse:
    stage = get_lead_assessment_stage_by_cycle_id(db, cycle_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Lead Assessment stage not found for the given cycle ID")
    
    return StageInfoResponse(
        start_date_of_stage=stage.start_date_of_stage,
        end_date_of_stage=stage.end_date_of_stage,
        is_active=stage.is_active,
        is_completed=stage.is_completed
        
    )

