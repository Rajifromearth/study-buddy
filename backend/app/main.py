from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as auth_router
from .routers.notes import router as notes_router
from .routers.qa import router as qa_router
from .routers.ask_ai import router as ask_ai_router
from .routers.learn_more import router as learn_more_router
from .routers.calendar import router as calendar_router
from .routers.study_plan import router as study_plan_router
from .routers.quiz import router as quiz_router

app = FastAPI(title="Study Buddy API")
app.add_middleware(
    CORSMiddleware,
    # TODO: Add the deployed frontend URL here before production; do not remove the local development origin.
    allow_origins=['http://localhost:5173', 'https://study-buddy-inky-gamma.vercel.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(qa_router)
app.include_router(ask_ai_router)
app.include_router(learn_more_router)
app.include_router(calendar_router)
app.include_router(study_plan_router)
app.include_router(quiz_router)

@app.get("/")
def read_root():
    return {"message": "Study Buddy backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
