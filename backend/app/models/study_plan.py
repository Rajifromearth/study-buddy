from pydantic import BaseModel


class StudyDay(BaseModel):
    date: str
    focus: str
    tasks: list[str]


class StudyPlan(BaseModel):
    id: str
    course: str
    target_date: str
    target_title: str
    created_at: str
    days: list[StudyDay]