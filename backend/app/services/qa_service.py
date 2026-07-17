import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .note_service import get_all_notes, get_notes_by_course


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def answer_question(question: str, course: str | None = None) -> dict:
    """Answer a question using only the text stored in selected notes."""
    notes = get_notes_by_course(course) if course else get_all_notes()
    if not notes:
        return {
            "answer": "No notes are available yet. Upload or add notes before asking a question.",
            "sources": [],
            "note": "No stored notes were available for this question.",
        }

    filenames = list(dict.fromkeys(note.filename for note in notes))
    context = "\n\n".join(
        f"--- Filename: {note.filename} ---\n{note.content}" for note in notes
    )
    prompt = f'''Answer the question using only the note context below. Do not use outside knowledge.
If the context does not contain the answer, say so clearly. Name the filename(s) you used.

Return valid JSON only with this shape:
{{"answer": "...", "sources": ["filename"], "note": "null or a brief explanation"}}
Only include filenames from the supplied context in sources.

Question: {question}

Note context:
{context}'''

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "The Q&A service is not configured yet.",
            "sources": [],
            "note": "Set OPENAI_API_KEY in backend/.env and try again.",
        }

    try:
        response = OpenAI(api_key=api_key).responses.create(
            model="gpt-5.6-terra", input=prompt
        )
        result = json.loads(response.output_text)
        sources = [name for name in result.get("sources", []) if name in filenames]
        return {
            "answer": str(result.get("answer", "")),
            "sources": sources,
            "note": result.get("note") or None,
        }
    except (json.JSONDecodeError, TypeError, ValueError):
        return {
            "answer": "The model returned an unexpected response format.",
            "sources": filenames,
            "note": "Please try asking the question again.",
        }
    except Exception as exc:
        print(f"QA service error: {exc}")
        return {
            "answer": "Unable to answer the question right now due to an AI service error.",
            "sources": [],
            "note": "Please check the API configuration and try again.",
        }