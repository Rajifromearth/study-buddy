from pydantic import BaseModel


class QuizQuestion(BaseModel):
    id: str
    question: str
    question_type: str
    options: list[str] | None = None
    correct_answer: str


class Quiz(BaseModel):
    id: str
    course: str
    source_note_id: str | None = None
    created_at: str
    questions: list[QuizQuestion]