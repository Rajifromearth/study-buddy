from pydantic import BaseModel


class Event(BaseModel):
    id: str
    title: str
    date: str
    event_type: str
    course: str | None = None
    source_note_id: str | None = None
    source_filename: str | None = None