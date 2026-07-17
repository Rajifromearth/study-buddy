from datetime import datetime
from pydantic import BaseModel

class Note(BaseModel):
    id: str
    filename: str
    course: str | None = None
    content: str
    uploaded_at: datetime
