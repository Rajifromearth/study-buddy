from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..models.study_plan import StudyPlan
from ..services.study_plan_service import generate_study_plan, get_study_plan, get_study_plans_by_course


router = APIRouter(prefix="/study-plan", tags=["study-plan"])


class StudyPlanRequest(BaseModel):
    course: str = Field(min_length=1)
    target_date: str = Field(min_length=1)
    target_title: str = Field(min_length=1)


@router.post("/generate", response_model=StudyPlan)
def generate_plan(payload: StudyPlanRequest) -> StudyPlan:
    return generate_study_plan(**payload.model_dump())


@router.get("/course/{course}", response_model=list[StudyPlan])
def list_course_plans(course: str) -> list[StudyPlan]:
    return get_study_plans_by_course(course)


@router.get("/{plan_id}", response_model=StudyPlan)
def get_plan(plan_id: str) -> StudyPlan:
    plan = get_study_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Study plan not found.")
    return plan