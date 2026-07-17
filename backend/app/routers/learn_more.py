from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..services.learn_more_service import expand_explanation


router = APIRouter(tags=["learn-more"])


class LearnMoreRequest(BaseModel):
    topic: str = Field(min_length=1)
    existing_content: str = Field(min_length=1)
    course: str | None = None


@router.post("/learn-more")
def learn_more(payload: LearnMoreRequest) -> dict:
    return expand_explanation(
        topic=payload.topic,
        existing_content=payload.existing_content,
        course=payload.course,
    )