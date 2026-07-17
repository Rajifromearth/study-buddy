from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field
from ..models.note  import Note
from ..services.note_service import extract_pdf_text, extract_txt_text, get_all_notes, get_notes_by_course, save_note

router = APIRouter(prefix="/notes", tags=["notes"])

class TextNoteRequest(BaseModel):
    content: str = Field(min_length=1)
    course: str | None = None
    filename: str = "pasted_note.txt"

@router.post("/upload", response_model=Note, status_code=status.HTTP_201_CREATED)
async def upload_note(file: UploadFile = File(...), course: str | None = Form(default=None)) -> Note:

    filename = file.filename or "uploaded_note"
    try:
        if Path(filename).suffix.lower() == ".pdf":
            content = extract_pdf_text(file.file)
        elif Path(filename).suffix.lower() == ".txt":
            content = extract_txt_text(file.file)
        else:
            raise HTTPException(status_code=400, detail="Only PDF and .txt files are supported.")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not extract text from the uploaded file.") from exc
    finally:
        await file.close()
    return save_note(filename=filename, course=course, content=content)

@router.post("/text", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_text_note(payload: TextNoteRequest) -> Note:
    return save_note(filename=payload.filename, course=payload.course, content=payload.content)

@router.get("", response_model=list[Note])
def list_notes() -> list[Note]:
    return get_all_notes()

@router.get("/{course}", response_model=list[Note])
def list_notes_for_course(course: str) -> list[Note]:
    return get_notes_by_course(course)
