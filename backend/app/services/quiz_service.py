import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI

from ..models.quiz import Quiz, QuizQuestion
from ..services.note_service import DATABASE_PATH, get_note_by_id, get_notes_by_course


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS quizzes (
        id TEXT PRIMARY KEY, course TEXT NOT NULL, source_note_id TEXT,
        created_at TEXT NOT NULL, questions TEXT NOT NULL)""")
    return connection


def _quiz(row: sqlite3.Row) -> Quiz:
    return Quiz(id=row["id"], course=row["course"], source_note_id=row["source_note_id"],
        created_at=row["created_at"],
        questions=[QuizQuestion(**question) for question in json.loads(row["questions"])])


def _save_quiz(quiz: Quiz) -> Quiz:
    with _connection() as connection:
        connection.execute("INSERT INTO quizzes VALUES (?, ?, ?, ?, ?)",
            (quiz.id, quiz.course, quiz.source_note_id, quiz.created_at,
             json.dumps([question.model_dump() for question in quiz.questions])))
    return quiz


def _fallback_quiz(course: str, note_id: str | None, message: str) -> Quiz:
    quiz = Quiz(id=str(uuid4()), course=course, source_note_id=note_id,
        created_at=datetime.now(timezone.utc).isoformat(), questions=[QuizQuestion(
            id=str(uuid4()), question=message, question_type="short_answer",
            options=None, correct_answer="Add course notes and generate the quiz again.")])
    return _save_quiz(quiz)


def _request_questions(content: str, num_questions: int) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Quiz service error: OPENAI_API_KEY is not configured.")
        return []
    prompt = f'''Create exactly {num_questions} practice questions from the note content below.
Use only the supplied content. Mix "multiple_choice" and "short_answer" questions when
possible. For multiple_choice, provide options and make correct_answer exactly match one
option. For short_answer, set options to null.

Return valid JSON only: a list of objects with question, question_type, options, and
correct_answer. question_type must be "multiple_choice" or "short_answer".

Note content:
{content}'''
    try:
        response = OpenAI(api_key=api_key).responses.create(model="gpt-5.6-terra", input=prompt)
        result = json.loads(response.output_text)
        return result if isinstance(result, list) else []
    except Exception as exc:
        print(f"Quiz service error: {exc}")
        return []


def generate_quiz(course: str, note_id: str | None = None, num_questions: int = 5) -> Quiz:
    source_note_id = note_id
    if note_id:
        note = get_note_by_id(note_id)
        notes = [note] if note else []
    else:
        notes = get_notes_by_course(course)
    content = "\n\n".join(f"--- {note.filename} ---\n{note.content}" for note in notes if note and note.content.strip())
    if not content:
        return _fallback_quiz(course, source_note_id, "No study material was found for this quiz.")

    questions = []
    for item in _request_questions(content, max(1, num_questions)):
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        answer = str(item.get("correct_answer", "")).strip()
        if not question or not answer:
            continue
        question_type = str(item.get("question_type", "short_answer")).strip()
        if question_type not in {"multiple_choice", "short_answer"}:
            question_type = "short_answer"
        options = item.get("options")
        if question_type == "multiple_choice" and isinstance(options, list):
            options = [str(option) for option in options]
        else:
            options = None
        questions.append(QuizQuestion(id=str(uuid4()), question=question,
            question_type=question_type, options=options, correct_answer=answer))

    if not questions:
        return _fallback_quiz(course, source_note_id, "Quiz generation could not create questions from the material.")
    quiz = Quiz(id=str(uuid4()), course=course, source_note_id=source_note_id,
        created_at=datetime.now(timezone.utc).isoformat(), questions=questions)
    return _save_quiz(quiz)


def get_quiz(quiz_id: str) -> Quiz | None:
    with _connection() as connection:
        row = connection.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    return _quiz(row) if row else None


def get_quizzes_by_course(course: str) -> list[Quiz]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM quizzes WHERE course = ? ORDER BY created_at DESC", (course,)).fetchall()
    return [_quiz(row) for row in rows]