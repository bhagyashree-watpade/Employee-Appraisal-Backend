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
            "stage_id":stage.stage_id,
            "stage_name": stage.stage_name,
            "start_date_of_stage": stage.start_date_of_stage,
            "end_date_of_stage": stage.end_date_of_stage
        }
        for stage in cycle.stages
    ]

  parameters = [
        {
            "parameter_id":param.parameter_id,
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


    cycle.cycle_name = data["cycle_name"]
    cycle.description = data["description"]
    cycle.status = data["status"]
    cycle.start_date_of_cycle = data["start_date_of_cycle"]
    cycle.end_date_of_cycle = data["end_date_of_cycle"]
    
    current_param_ids = [param["parameter_id"] for param in data.get("parameters", []) if param.get("parameter_id")]

    # Delete parameters not included in the frontend data
    if current_param_ids:
        db.query(Parameter).filter(
        Parameter.cycle_id == cycle_id,
        Parameter.parameter_id.notin_(current_param_ids)
        ).delete(synchronize_session=False)

    for param in data.get("parameters", []):
        param_id = param.get("parameter_id") 
        if param_id:
            existing_param = db.query(Parameter).filter(
                Parameter.parameter_id == param_id,
                Parameter.cycle_id == cycle_id
            ).first()
            if existing_param:
                existing_param.parameter_title = param["name"]
                existing_param.helptext = param.get("helptext", "")
                existing_param.applicable_to_employee = param["employee"]
                existing_param.applicable_to_lead = param["teamLead"]
                existing_param.is_fixed_parameter = param["fixed"]
            else:
                db.add(Parameter(
                    parameter_title=param["name"],
                    helptext=param.get("helptext", ""),
                    cycle_id=cycle_id,
                    applicable_to_employee=param["employee"],
                    applicable_to_lead=param["teamLead"],
                    is_fixed_parameter=param["fixed"]
                ))
        else:
            db.add(Parameter(
                parameter_title=param["name"],
                helptext=param.get("helptext", ""),
                cycle_id=cycle_id,
                applicable_to_employee=param["employee"],
                applicable_to_lead=param["teamLead"],
                is_fixed_parameter=param["fixed"]
            ))

    for stage in data.get("stages", []):
        stage_id = stage.get("stage_id")  
        if stage_id:
            existing_stage = db.query(Stage).filter(
                Stage.stage_id == stage_id,
                Stage.cycle_id == cycle_id
            ).first()
            if existing_stage:
                existing_stage.stage_name = stage["name"]
                existing_stage.start_date_of_stage = stage.get("startDate")
                existing_stage.end_date_of_stage = stage.get("endDate")


    db.commit()
    db.refresh(cycle)

    return {"message": "Appraisal cycle updated successfully"}