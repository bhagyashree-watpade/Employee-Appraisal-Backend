from sqlalchemy.orm import Session
from models.appraisal_cycle import AppraisalCycle
from models.stages import Stage
from models.parameters import Parameter
from models.edit_appraisal_cycle import CycleUpdate
from schema.edit_appraisal_cycle import GetAppraisalCycleResponse
from fastapi import HTTPException

def get_cycle(db:Session, cycle_id:int):
  cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()

  if not cycle:
      raise HTTPException(status_code=404, detail="Appraisal cycle not found")

  stages = [
        {
            "stage_name": stage.stage_name,
            "start_date_of_stage": stage.start_date_of_stage,
            "end_date_of_stage": stage.end_date_of_stage
        }
        for stage in cycle.stages
    ]

  parameters = [
        {
            "parameter_title": param.parameter_title,
            "helptext": param.helptext,
            "cycle_id": param.cycle_id,
            "applicable_to_employee": param.applicable_to_employee,
            "applicable_to_lead": param.applicable_to_lead,
            "is_fixed_parameter": param.is_fixed_parameter
        }
        for param in cycle.parameters
    ]

  return GetAppraisalCycleResponse(
        cycle_id=cycle.cycle_id,
        cycle_name=cycle.cycle_name,
        description=cycle.description,
        status=cycle.status,
        start_date_of_cycle=cycle.start_date_of_cycle,
        end_date_of_cycle=cycle.end_date_of_cycle,
        stages=stages,
        parameters=parameters
    )

def edit_cycle(db: Session, cycle_id: int, cycle_data: CycleUpdate):
    data = cycle_data.dict()

    cycle = db.query(AppraisalCycle).filter(AppraisalCycle.cycle_id == cycle_id).first()

    if not cycle:
        raise HTTPException(status_code=404, detail="Appraisal cycle not found")

    # Update cycle fields
    cycle.cycle_name = data["cycle_name"]
    cycle.description = data["description"]
    cycle.status = data["status"]
    cycle.start_date_of_cycle = data["start_date_of_cycle"]
    cycle.end_date_of_cycle = data["end_date_of_cycle"]

    # Delete old parameters and insert new
    db.query(Parameter).filter(Parameter.cycle_id == cycle_id).delete()
    for param in data.get("parameters", []):
        db.add(Parameter(
            parameter_title=param["name"],
            helptext=param.get("helptext", ""),
            cycle_id=cycle_id,
            applicable_to_employee=param["employee"],
            applicable_to_lead=param["teamLead"],
            is_fixed_parameter=param["fixed"]
        ))

    # Delete old stages and insert new
    db.query(Stage).filter(Stage.cycle_id == cycle_id).delete()
    for stage in data.get("stages", []):
        db.add(Stage(
            stage_name=stage["name"],
            start_date_of_stage=stage.get("startDate"),
            end_date_of_stage=stage.get("endDate"),
            cycle_id=cycle_id
        ))

    # Commit all changes
    db.commit()
    db.refresh(cycle)

    return {"message": "Appraisal cycle updated successfully"}
