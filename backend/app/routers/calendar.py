from fastapi import APIRouter

from ..models.event import Event
from ..services.calendar_service import (
    extract_dates_from_course,
    extract_dates_from_note,
    get_all_events,
    get_events_by_course,
)


router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("/extract/note/{note_id}", response_model=list[Event])
def extract_note_dates(note_id: str) -> list[Event]:
    return extract_dates_from_note(note_id)


@router.post("/extract/course/{course}", response_model=list[Event])
def extract_course_dates(course: str) -> list[Event]:
    return extract_dates_from_course(course)


@router.get("/events", response_model=list[Event])
def list_events() -> list[Event]:
    return get_all_events()


@router.get("/events/{course}", response_model=list[Event])
def list_course_events(course: str) -> list[Event]:
    return get_events_by_course(course)