from fastapi import FastAPI

app = FastAPI(title="Study Buddy API")

@app.get("/")
def read_root():
    return {"message": "Study Buddy backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}