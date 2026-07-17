import json
import os
import sqlite3
from datetime import date
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI

from ..models.event import Event
from ..services.note_service import DATABASE_PATH, get_all_notes, get_note_by_id, get_notes_by_course


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY, title TEXT NOT NULL, date TEXT NOT NULL,
        event_type TEXT NOT NULL, course TEXT, source_note_id TEXT,
        source_filename TEXT)""")
    return connection


def _event(row: sqlite3.Row) -> Event:
    return Event(id=row["id"], title=row["title"], date=row["date"],
        event_type=row["event_type"], course=row["course"],
        source_note_id=row["source_note_id"], source_filename=row["source_filename"])


def _extract_items(content: str) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Calendar service error: OPENAI_API_KEY is not configured.")
        return []
    prompt = f'''Extract only dated academic events from this note. Include exams, assignments,
deadlines, and other important dates. Convert every date to YYYY-MM-DD when the note
contains enough date information. Do not infer dates that are not present.

Return valid JSON only: a list of objects with title, date, and event_type. event_type
must be one of "exam", "assignment", "deadline", or "other". Return [] if none exist.

Note content:
{content}'''
    try:
        response = OpenAI(api_key=api_key).responses.create(model="gpt-5.6-terra", input=prompt)
        items = json.loads(response.output_text)
        return items if isinstance(items, list) else []
    except Exception as exc:
        print(f"Calendar service error: {exc}")
        return []


def _save_event(item: dict, note, course: str | None) -> Event | None:
    title = str(item.get("title", "")).strip()
    event_date = str(item.get("date", "")).strip()
    event_type = str(item.get("event_type", "other")).strip().lower()
    if not title or not event_date:
        return None
    try:
        date.fromisoformat(event_date)
    except ValueError:
        return None
    if event_type not in {"exam", "assignment", "deadline", "other"}:
        event_type = "other"
    with _connection() as connection:
        existing = connection.execute(
            "SELECT id FROM events WHERE lower(title) = lower(?) AND date = ? "
            "AND ((course = ?) OR (course IS NULL AND ? IS NULL))",
            (title, event_date, course, course),
        ).fetchone()
        if existing:
            return None
        event = Event(id=str(uuid4()), title=title, date=event_date,
            event_type=event_type, course=course, source_note_id=note.id,
            source_filename=note.filename)
        connection.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)",
            (event.id, event.title, event.date, event.event_type, event.course,
             event.source_note_id, event.source_filename))
    return event


def extract_dates_from_note(note_id: str) -> list[Event]:
    note = get_note_by_id(note_id)
    if not note:
        print(f"Calendar service error: note {note_id} was not found.")
        return []
    events = []
    for item in _extract_items(note.content):
        if isinstance(item, dict):
            event = _save_event(item, note, note.course)
            if event:
                events.append(event)
    return events


def extract_dates_from_course(course: str) -> list[Event]:
    events = []
    seen = set()
    for note in get_notes_by_course(course):
        for item in _extract_items(note.content):
            if not isinstance(item, dict):
                continue
            key = (str(item.get("title", "")).strip().lower(), str(item.get("date", "")).strip())
            if not key[0] or not key[1] or key in seen:
                continue
            seen.add(key)
            event = _save_event(item, note, course)
            if event:
                events.append(event)
    return events


def get_all_events() -> list[Event]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM events ORDER BY date ASC, title ASC").fetchall()
    return [_event(row) for row in rows]


def get_events_by_course(course: str) -> list[Event]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM events WHERE course = ? ORDER BY date ASC, title ASC", (course,)).fetchall()
    return [_event(row) for row in rows]