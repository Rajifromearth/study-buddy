from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..models.quiz import Quiz
from ..services.quiz_service import generate_quiz, get_quiz, get_quizzes_by_course


router = APIRouter(prefix="/quiz", tags=["quiz"])


class QuizRequest(BaseModel):
    course: str = Field(min_length=1)
    note_id: str | None = None
    num_questions: int = Field(default=5, ge=1)


@router.post("/generate", response_model=Quiz)
def generate_course_quiz(payload: QuizRequest) -> Quiz:
    return generate_quiz(**payload.model_dump())


@router.get("/course/{course}", response_model=list[Quiz])
def list_course_quizzes(course: str) -> list[Quiz]:
    return get_quizzes_by_course(course)


@router.get("/{quiz_id}", response_model=Quiz)
def get_saved_quiz(quiz_id: str) -> Quiz:
    quiz = get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return quiz