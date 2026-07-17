from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..services.ask_ai_service import ask_general


router = APIRouter(tags=["ask-ai"])


class AskAIRequest(BaseModel):
    question: str = Field(min_length=1)
    course: str | None = None


@router.post("/ask-ai")
def ask_ai(payload: AskAIRequest) -> dict:
    return ask_general(question=payload.question, course=payload.course)