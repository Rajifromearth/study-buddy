from fastapi import APIRouter
from pydantic import BaseModel, Field

from ..services.qa_service import answer_question


router = APIRouter(prefix="/qa", tags=["qa"])


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    course: str | None = None


@router.post("/ask")
def ask_question(payload: QuestionRequest) -> dict:
    return answer_question(question=payload.question, course=payload.course)