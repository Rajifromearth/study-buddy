import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO
from uuid import uuid4
from pypdf import PdfReader
from ..models.note import Note

DATABASE_PATH = Path(__file__).resolve().parents[2] / "study_buddy.db"

def _connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""CREATE TABLE IF NOT EXISTS notes (
        id TEXT PRIMARY KEY, filename TEXT NOT NULL, course TEXT,
        content TEXT NOT NULL, uploaded_at TEXT NOT NULL)""")
    return connection

def extract_pdf_text(file: BinaryIO) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(file).pages).strip()

def extract_txt_text(file: BinaryIO) -> str:
    raw_content = file.read()
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            return raw_content.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    raise ValueError("The uploaded text file must be UTF-8 or UTF-16 encoded.")

def save_note(*, filename: str, content: str, course: str | None = None) -> Note:
    note = Note(id=str(uuid4()), filename=filename, course=course or None,
                content=content, uploaded_at=datetime.now(timezone.utc))
    with _connection() as connection:
        connection.execute("INSERT INTO notes VALUES (?, ?, ?, ?, ?)",
            (note.id, note.filename, note.course, note.content, note.uploaded_at.isoformat()))
    return note

def _note(row: sqlite3.Row) -> Note:
    return Note(id=row["id"], filename=row["filename"], course=row["course"],
        content=row["content"], uploaded_at=datetime.fromisoformat(row["uploaded_at"]))

def get_all_notes() -> list[Note]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM notes ORDER BY uploaded_at DESC").fetchall()
    return [_note(row) for row in rows]

def get_notes_by_course(course: str) -> list[Note]:
    with _connection() as connection:
        rows = connection.execute("SELECT * FROM notes WHERE course = ? ORDER BY uploaded_at DESC", (course,)).fetchall()
    return [_note(row) for row in rows]


def get_note_by_id(note_id: str) -> Note | None:
    with _connection() as connection:
        row = connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return _note(row) if row else None