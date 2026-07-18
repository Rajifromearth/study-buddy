# Study Buddy

A study companion that turns your own notes and syllabus into an active study tool — ask questions, get an auto-built calendar, a day-by-day study plan, and practice quizzes, all generated from material you actually uploaded.

Built for **OpenAI Build Week** (Devpost hackathon, July 13–21, 2026), Education track, using **Codex** and **GPT-5.6**.

## The problem

Students take notes and get syllabi, but the information just sits there — untracked deadlines, no clear study plan, and no fast way to find something you know you wrote down somewhere. Study Buddy closes that gap by reading your own material and turning it into something actionable.

## Tech stack

- **Backend:** FastAPI (Python 3.14)
- **Frontend:** React/Vite (in progress, built by teammate)
- **Database:** SQLite (single-file, zero-setup)
- **AI:** OpenAI GPT-5.6 via the Responses API
- **Dev tooling:** Codex (VS Code extension + CLI) used to scaffold and implement all backend features

## Architecture

```
backend/
└── app/
    ├── main.py                 # FastAPI app entrypoint, wires up all routers
    ├── models/                 # Pydantic data models
    │   ├── note.py
    │   ├── event.py
    │   ├── study_plan.py
    │   └── quiz.py
    ├── services/                # Business logic + OpenAI calls + SQLite persistence
    │   ├── note_service.py
    │   ├── qa_service.py
    │   ├── calendar_service.py
    │   ├── study_plan_service.py
    │   └── quiz_service.py
    └── routers/                 # FastAPI route definitions
        ├── notes.py
        ├── qa.py
        ├── calendar.py
        ├── study_plan.py
        └── quiz.py
```

All AI-powered services follow the same consistent pattern:
1. Load `OPENAI_API_KEY` from `backend/.env` via `python-dotenv`
2. Call GPT-5.6 through the OpenAI Responses API, requesting structured JSON output
3. Validate and sanitize whatever comes back (dates, enums, required fields) before saving
4. Fail gracefully — never crash, always return a safe fallback, log the real error to the console for debugging
5. Persist to SQLite (`backend/study_buddy.db`), created automatically on first run

## Features built so far

### 1. Notes Ingestion
Upload notes as a PDF or `.txt` file, or paste text directly. Notes are tagged by course and stored for every other feature to use.

- `POST /notes/upload` — upload a PDF or .txt file
- `POST /notes/text` — submit pasted text directly
- `GET /notes` — list all notes
- `GET /notes/{course}` — list notes for a specific course

### 2. Q&A on Your Notes
Ask a question and get an answer generated strictly from your own uploaded material — not general knowledge. The response cites which note(s) the answer came from, and says so honestly if the notes don't contain an answer.

- `POST /qa/ask` — body: `{ question, course }`

### 3. Auto-Calendar / Date Extraction
Feed in notes or a syllabus and GPT-5.6 extracts exams, assignments, and deadlines automatically — no manual date entry. Duplicate events (same title + date) are filtered out.

- `POST /calendar/extract/note/{note_id}` — extract dates from a single note
- `POST /calendar/extract/course/{course}` — extract dates across every note in a course
- `GET /calendar/events` — list all events
- `GET /calendar/events/{course}` — list events for a course

### 4. Study Plan Generator
Given a target date and a course, generates a day-by-day study plan working backward from the deadline, referencing actual topics from your notes. Handles edge cases cleanly: invalid dates, past dates, and courses with no notes yet all return a sensible plan instead of an error.

- `POST /study-plan/generate` — body: `{ course, target_date, target_title }`
- `GET /study-plan/{plan_id}`
- `GET /study-plan/course/{course}`

### 5. Quiz / Flashcard Generator
Generates a mix of multiple-choice and short-answer practice questions from a course's notes (or a single note), with correct answers included — turns passive notes into active self-testing.

- `POST /quiz/generate` — body: `{ course, note_id, num_questions }`
- `GET /quiz/{quiz_id}`
- `GET /quiz/course/{course}`

## Setup

```powershell
# Clone and enter the project
cd "STUDY BUDDY"

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend\requirements.txt

# Add your OpenAI API key
# Create backend/.env with:
# OPENAI_API_KEY=sk-your-key-here

# Run the server
uvicorn backend.app.main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for interactive API docs (Swagger UI) to explore and test every endpoint.

## How Codex and GPT-5.6 were used

- **Codex** scaffolded and implemented every backend feature in this repo — models, services, and routers — from detailed prompts specifying exact function signatures, error-handling patterns, and import conventions, following a consistent style established across the codebase.
- **GPT-5.6** powers the app itself at runtime: answering questions from notes, extracting calendar dates, generating study plans, and generating quiz questions — all via the OpenAI Responses API.

## Status

All five backend features are implemented and code-reviewed. End-to-end testing against the live GPT-5.6 API is in progress, pending OpenAI API credit.

## What's next

- Frontend integration (React/Vite) 
- End-to-end testing of all AI-powered endpoints
- Possible additions if time allows: progress tracking, weak-spot detection based on Q&A history
- Deploy: backend to Render, frontend to Vercel