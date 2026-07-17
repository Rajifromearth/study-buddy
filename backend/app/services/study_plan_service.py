import json
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI

from ..models.study_plan import StudyDay, StudyPlan
from ..services.note_service import DATABASE_PATH, get_notes_by_course


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS study_plans (
        id TEXT PRIMARY KEY, course TEXT NOT NULL, target_date TEXT NOT NULL,
        target_title TEXT NOT NULL, created_at TEXT NOT NULL, days TEXT NOT NULL)""")
    return connection


def _plan(row: sqlite3.Row) -> StudyPlan:
    return StudyPlan(id=row["id"], course=row["course"], target_date=row["target_date"],
        target_title=row["target_title"], created_at=row["created_at"],
        days=[StudyDay(**day) for day in json.loads(row["days"])])


def _save_plan(plan: StudyPlan) -> StudyPlan:
    with _connection() as connection:
        connection.execute("INSERT INTO study_plans VALUES (?, ?, ?, ?, ?, ?)",
            (plan.id, plan.course, plan.target_date, plan.target_title,
             plan.created_at, json.dumps([day.model_dump() for day in plan.days])))
    return plan


def _request_days(course: str, target_date: str, target_title: str, days_remaining: int,
                  context: str) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Study plan service error: OPENAI_API_KEY is not configured.")
        return []
    prompt = f'''Create a day-by-day study plan for course "{course}" through {target_date}
for "{target_title}". There are {days_remaining} days remaining. Use actual topics from
the notes where possible. Include every calendar day from today through the target date.

Return valid JSON only: a list of objects with date (YYYY-MM-DD), focus (short summary),
and tasks (list of strings). Do not use knowledge outside the supplied notes.

Notes:
{context}'''
    try:
        response = OpenAI(api_key=api_key).responses.create(model="gpt-5.6-terra", input=prompt)
        result = json.loads(response.output_text)
        return result if isinstance(result, list) else []
    except Exception as exc:
        print(f"Study plan service error: {exc}")
        return []


def generate_study_plan(course: str, target_date: str, target_title: str) -> StudyPlan:
    today = date.today()
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        target = date.fromisoformat(target_date)
    except ValueError:
        print(f"Study plan service error: invalid target date {target_date}.")
        plan = StudyPlan(id=str(uuid4()), course=course, target_date=target_date,
            target_title=target_title, created_at=created_at,
            days=[StudyDay(date=today.isoformat(), focus="Invalid target date",
                tasks=["Use an ISO date in YYYY-MM-DD format to generate a study plan."])])
        return _save_plan(plan)

    if target <= today:
        plan = StudyPlan(id=str(uuid4()), course=course, target_date=target_date,
            target_title=target_title, created_at=created_at,
            days=[StudyDay(date=today.isoformat(), focus="Target date has passed",
                tasks=["The target date is today or in the past. Choose a future date to create a study plan."])])
        return _save_plan(plan)

    notes = get_notes_by_course(course)
    no_notes = not notes
    context = "\n\n".join(f"--- {note.filename} ---\n{note.content}" for note in notes)
    generated = _request_days(course, target_date, target_title, (target - today).days, context)
    by_date = {}
    for item in generated:
        if not isinstance(item, dict):
            continue
        try:
            item_date = date.fromisoformat(str(item.get("date", "")))
        except ValueError:
            continue
        if today <= item_date <= target:
            tasks = item.get("tasks", [])
            by_date[item_date.isoformat()] = StudyDay(date=item_date.isoformat(),
                focus=str(item.get("focus", "General review")),
                tasks=[str(task) for task in tasks] if isinstance(tasks, list) else [str(tasks)])

    days = []
    current = today
    while current <= target:
        day = by_date.get(current.isoformat())
        if not day:
            day = StudyDay(date=current.isoformat(), focus="General review",
                tasks=["Review course material and prepare for the target."])
        days.append(day)
        current += timedelta(days=1)
    if no_notes:
        days[0].tasks.insert(0, "No notes were found for this course; general review is recommended.")

    plan = StudyPlan(id=str(uuid4()), course=course, target_date=target_date,
        target_title=target_title, created_at=created_at, days=days)
    return _save_plan(plan)


def get_study_plan(plan_id: str) -> StudyPlan | None:
    with _connection() as connection:
        row = connection.execute("SELECT * FROM study_plans WHERE id = ?", (plan_id,)).fetchone()
    return _plan(row) if row else None


def get_study_plans_by_course(course: str) -> list[StudyPlan]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM study_plans WHERE course = ? ORDER BY created_at DESC", (course,)).fetchall()
    return [_plan(row) for row in rows]